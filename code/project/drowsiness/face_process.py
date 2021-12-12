import os
import cv2
import dlib
import sys
import time
import numpy as np
from parameters import *
# from threading import Thread
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
yawn_counter = 0
drowsy = False
yawn = False
distracted = False

# def sound_alarm(sound_queue):
#     global CODERUN
#     while CODERUN:
#         alarm_message = sound_queue.get(block=True)
#         # cmd = f'espeak -ven+f2 -k5 -s150 --stdout  "{alarm_message}" | aplay '
#         # os.system(cmd)
#         # time.sleep(3)

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
#def eye_rect(eye):
#   x1 = eye[0]
#   x2 = eye[3]
#   y1 = eye[1]
#   y2 = eye[5]
#   return [x1, x2, y1, y2]

# lerect = eye_rect(leftEye)
# eye_frame = frame[lerect[0]:lerect[1], lerect[2]:lerect[3]]
# cv2.imshow('eye_frame', eye_frame)
# gray2 = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)


#computes the mouth aspect ratio (mar)
def get_mouth_aspect_ratio(mouth):
    # mouth landmarks (x, y)-coordinates
    horizontal=distance.euclidean(mouth[0],mouth[4])
    vertical=0
    for coord in range(1,4):
        vertical+=distance.euclidean(mouth[coord],mouth[8-coord])
    #return MAR
    return vertical/(horizontal*3)


def image_put(image_queque):
    cap =cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
    global CODERUN
    while CODERUN:
        image_queque.put(cap.read()[1])
        image_queque.get() if image_queque.qsize() > 1 else time.sleep(0.01)
        
def image_get(process_queue):
    os.environ['DISPLAY'] = ":0.0"
    print(os.environ['DISPLAY'])
    global CODERUN
    while CODERUN:
        frame = process_queue.get()
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(5)&0xFF
	
	# # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        #  pass
    

# Facial processing
def facial_processing(image_queue, process_queue, sound_queue):
    global distracted_counter, drowsy_counter, yawn_counter
    global distracted, yawn, drowsy
    global CODERUN
    # distracton_initialized   = False
    # eye_initialized          = False
    # mouth_initialized        = False
	
    #get face detector and facial landmark predector
    detector    = dlib.get_frontal_face_detector()
    predictor   = dlib.shape_predictor(shape_predictor_path)

    
    #d grab the indexes of the facial landmarks for the left an right eye, respectively
    ls,le = face.FACIAL_LANDMARKS_IDXS["left_eye"]
    rs,re = face.FACIAL_LANDMARKS_IDXS["right_eye"]
    
    # loop over frames from the video stream
    while CODERUN:
        # time.sleep(0.2)
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
                print("EYE_ON_ROAD")
                f.write("EYE_ON_ROAD\n")
            
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
        #gets the MAR for mouth
            inner_lips=shape[60:68]
            mar=get_mouth_aspect_ratio(inner_lips)
	    # compute the convex hull for the left and right eye, then
	    # visualize each of the eyes, draw bounding boxes around eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (255, 255, 255), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (255, 255, 255), 1)
            lipHull = cv2.convexHull(inner_lips)
            cv2.drawContours(frame, [lipHull], -1, (255, 255, 255), 1)
	    #display EAR on screens
            cv2.putText(frame, "EAR: {:.2f} MAR{:.2f}".format(eye_aspect_ratio,mar), (10, frame.shape[0]-10),\
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
	    #checking if eyes are drooping/almost closed
            if eye_aspect_ratio < EYE_DROWSINESS_THRESHOLD:
                drowsy_counter += 1
                if drowsy_counter >= 10:
                    drowsy = True
                    print("DROWSY")
                    f.write("DROWSY\n")
                    drowsy_counter = 0
                    # alarm_message = "Drowsing"
                    # sound_queue.put(alarm_message)
                if drowsy:
                    cv2.putText(frame, "YOU ARE DROWSY!", (10, 30),
                                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
            else:
                if drowsy:
                    drowsy = False
                    drowsy_counter = 0
                    print("NOT_DROWSY")
                    f.write("NOT_DROWSY\n")
                                
	    #checks if user is yawning
            if mar > MOUTH_DROWSINESS_THRESHOLD:
                yawn_counter += 1
                if yawn_counter >= 5:
                    yawn = True
                    print("YAWN")
                    f.write("YAWN\n")
                    # alarm_message = "Yawning"
                    # sound_queue.put(alarm_message)
                    yawn_counter = 0
                if yawn:
                    cv2.putText(frame, "YOU ARE YAWNING!", (10, 70),
                                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                if yawn:
                    yawn = False
                    print("NOT_YAWN")
                    f.write("NOT_YAWN\n")
                    yawn_counter = 0
  
	#if the user's face is not focused on the road, the eyes/mouth features cannot be computed
        else:
            distracted_counter += 1
            if distracted_counter >= 20:
                f.write("EYE_OFF_ROAD\n")
                print("EYE_OFF_ROAD")
                distracted = True
                drowsy = False
                yawn = False
                drowsy_counter = 0
                yawn_counter = 0
                distracted_counter = 0
                # alarm_message = "Distracting"
                # sound_queue.put(alarm_message)
            if distracted:
                cv2.putText(frame, "PLEASE KEEP EYES ON ROAD", (10, 30),
                                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
        # pass the frame to image_get
        process_queue.put(frame)
        process_queue.get() if process_queue.qsize() > 1 else time.sleep(0.01)
	

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
        # process4 = Process(target=sound_alarm, args=(sound_queue, ))
        # process4.daemon = True
        process1.start()
        process2.start()
        process3.start()
        # process4.start()
        process1.join()
        process2.join()
        process3.join()
        # process4.join()
        print("End All Process!")
    except KeyboardInterrupt:
        try:
            print("Exit Face Process ")
            sys.exit(0)
        except SystemExit:
            os._exit(0)
