import os
import cv2
import dlib
import sys
import time
import numpy as np
from parameters import *
from datetime import datetime
from scipy.spatial import distance
from imutils import face_utils as face
from multiprocessing import Queue, Process
from PIL import Image
import RPi.GPIO as GPIO

CODERUN = True

#setting the GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def GPIO27_callback(channel):
    global CODERUN
    print("Button 27 has been pressed, quit the face_process program\n")
    CODERUN = False
    GPIO.cleanup()
    sys.exit(0)
    
distracted_counter = 0
drowsy_counter = 0
eye_track_counter = 0
drowsy = False
eye_track = False
distracted = False

cap =cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))

#draw a bounding box over face
def get_max_area_rect(rects):
    # checks to see if a face was not dectected (0)
    if len(rects)==0: return
    areas=[]
    for rect in rects:
        areas.append(rect.area())
    return rects[areas.index(max(areas))]

#computes the eye aspect ratio (ear)
def get_eye_aspect_ratio(eye):
    # eye landmarks (x, y)-coordinates
    vertical_1 = distance.euclidean(eye[1], eye[5])
    vertical_2 = distance.euclidean(eye[2], eye[4])
    horizontal = distance.euclidean(eye[0], eye[3])
    #returns EAR
    return (vertical_1+vertical_2)/(horizontal*2)

#computes rect for eye
def eye_rect(eye):
    x1 = eye[0][0]
    x2 = eye[3][0]
    y1 = eye[1][1]
    y2 = eye[5][1]
    return [x1, x2, y1, y2]

def image_put(image_queque):
    global CODERUN
    while CODERUN:
        image_queque.put(cap.read()[1])
        image_queque.get() if image_queque.qsize() > 1 else time.sleep(0.01)
        
def image_get(process_queue):
    os.environ['DISPLAY'] = ":0.0"
    # print(os.environ['DISPLAY'])
    global CODERUN
    while CODERUN:
        frame = process_queue.get()
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(5)&0xFF
	
	# # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

# Facial processing
def facial_processing(image_queue, process_queue, sound_queue):
    global distracted_counter, drowsy_counter, eye_track_counter
    global distracted, drowsy
    global CODERUN
	
    #get face detector and facial landmark predector
    detector    = dlib.get_frontal_face_detector()
    predictor   = dlib.shape_predictor(shape_predictor_path)

    #d grab the indexes of the facial landmarks for the left an right eye, respectively
    ls,le = face.FACIAL_LANDMARKS_IDXS["left_eye"]
    rs,re = face.FACIAL_LANDMARKS_IDXS["right_eye"]
    try:
        # loop over frames from the video stream
        while CODERUN:
            time.sleep(0.2)
            f = open("message.txt", "a+")
            frame = image_queue.get()
        #flip around y-axis
            frame = cv2.flip(frame, 1)
        #convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # detect faces in the grayscale frame
            rects = detector(gray, 0)
        #draw bounding box on face
            rect=get_max_area_rect(rects)   
            
            if rect!=None:
                if distracted:
                    distracted_counter = 0
                    distracted = False
                    print("HEAD_ON_ROAD")
                    f.write("HEAD_ON_ROAD\n")
                
            # determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
                shape = predictor(gray, rect)
                shape = face.shape_to_np(shape)
            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
                leftEye = shape[ls:le]
                rightEye = shape[rs:re]
            #gets the EAR for each eye
                leftEAR = get_eye_aspect_ratio(leftEye)
                rightEAR = get_eye_aspect_ratio(rightEye)
            # average the eye aspect ratio together for both eyes
                eye_aspect_ratio = (leftEAR + rightEAR) / 2.0
            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes, draw bounding boxes around eyes
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (255, 255, 255), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (255, 255, 255), 1)
                cv2.putText(frame, "EAR: {:.2f} ".format(eye_aspect_ratio), (10, frame.shape[0]-10),\
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            #checking if eyes are drooping/almost closed
                if eye_aspect_ratio < EYE_DROWSINESS_THRESHOLD:
                    drowsy_counter += 1
                    if drowsy_counter >= 10:
                        drowsy = True
                        print("DROWSY")
                        f.write("DROWSY\n")
                        drowsy_counter = 0
                    if drowsy:
                        cv2.putText(frame, "YOU ARE DROWSY!", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        
                else:
                    if drowsy:
                        drowsy = False
                        drowsy_counter = 0
                        print("NOT_DROWSY")
                        f.write("NOT_DROWSY\n")
                        
                lerect = eye_rect(leftEye)
                #calculate x mid distance of left eye
                mid = distance.euclidean(lerect[0],lerect[1])/2
                #crop each frame to only show left eye
                eye_frame = frame[lerect[2]:lerect[3], lerect[0]:lerect[1]]
                #inversion & greyscale
                eye_frame = cv2.bitwise_and(eye_frame, eye_frame)
                gray2     = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
                #adaptive thresholding to delineate iris from white of eyes
                th_left   = cv2.adaptiveThreshold(gray2, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 45)
                #find contours of iris
                cnts, _   = cv2.findContours(th_left, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
                try:
                    cnt = max(cnts, key = cv2.contourArea)
                    #calculate moments of binary image
                    M = cv2.moments(cnt)
                    #calculate x/y coordinate of contour center 
                    cX = int(M["m10"]/ M["m00"])
                    cY = int(M['m01']/M['m00'])
                    cv2.circle(eye_frame, (cX, cY), 7, (255, 255, 0), 2)
                    #if the absolute difference between the mid distance and the iris center is > 10 ...
                    if abs(mid-cX) > 10:            
                        print("Looking Away")
                        #person is looking away and start counter
                        eye_track_counter += 1
                        if eye_track_counter > 4: 
                            eye_track = True
                            drowsy = False
                            drowsy_counter = 0
                            print("EYE_OFF_ROAD")
                            f.write("EYE_OFF_ROAD\n")
                            eye_track_counter = 0
                        if eye_track:
                            cv2.putText(frame, "KEEP EYES ON THE ROAD!", (10, 70),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    else:
                        if eye_track:
                            eye_track = False
                            print("EYE_ON_ROAD")
                            f.write("EYE_ON_ROAD\n")
                            eye_track_counter = 0        
                except:
                    pass
                
    
        #if the user's face is not focused on the road, the eyes/mouth features cannot be computed
            else:
                distracted_counter += 1
                if distracted_counter >= 20:
                    f.write("HEAD_OFF_ROAD\n")
                    print("HEAD_OFF_ROAD")
                    distracted = True
                    drowsy = False
                    drowsy_counter = 0
                    distracted_counter = 0
                if distracted:
                    cv2.putText(frame, "PLEASE FACE THE ROAD", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
            # pass the frame to image_get
            process_queue.put(frame)
            process_queue.get() if process_queue.qsize() > 1 else time.sleep(0.01)
    except KeyboardInterrupt: 
        try:
            print("Exit Face Process ")
            sys.exit(0)
        except SystemExit:
            os._exit(0)
	
 

if __name__=='__main__':
    GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=500)
    try:
        image_queue = Queue()
        process_queue = Queue()
        sound_queue = Queue()
        process1 = Process(target=image_put, args=(image_queue,))
        process1.daemon = True
        process2 = Process(target=image_get, args=(process_queue,))
        process2.daemon = True
        process3 = Process(target=facial_processing, args=(image_queue, process_queue, sound_queue,))
        process3.daemon = True
        process1.start()
        process2.start()
        process3.start()
        process1.join()
        process2.join()
        process3.join()
        print("End All Process!")
    except KeyboardInterrupt:
        try:
            print("Exit Face Process ")
            cap.release()
            sys.exit(0)
        except SystemExit:
            cap.release()
            os._exit(0)
