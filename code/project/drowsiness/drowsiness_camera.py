import os
import cv2
import dlib
import sys
import time
import board
import RPi.GPIO as GPIO

import busio
import adafruit_mpr121
import numpy as np
from parameters import *
# from threading import Thread
from datetime import datetime
from scipy.spatial import distance
from imutils import face_utils as face
from multiprocessing import Queue, Process
from PIL import Image

# from pygame.locals import *
import RPi.GPIO as GPIO
import pygame

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

os.environ['DISPLAY'] = ':0'
# set up the enviroments
# os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
# os.putenv('SDL_FBDEV', '/dev/fb1')
# os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
# os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def GPIO17_callback(channel): 
    global CodeRun
    GPIO.cleanup()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
    
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)


# pygame.init()
# screen = pygame.display.set_mode((320,240))
# my_font = pygame.font.Font(None,26)
# white = 255,255,255
# black = 0,0,0
# green = 0,255,0
# red = 255,0,0

# drowsy_alert = my_font.render("Drowsy", True, white)
# rect_drowsy_alert = drowsy_alert.get_rect(center = (80,60))
# distracted_alert = my_font.render("Looking Away", True, white)
# rect_distracted_alert = distracted_alert.get_rect(center = (240,60))
# wheel_alert = my_font.render("Steering Wheel", True, white)
# rect_wheel_alert = wheel_alert.get_rect(center = (80,180))
# collision_alert = my_font.render("Collision", True, white)
# rect_collision_alert = collision_alert.get_rect(center = (240,180))

# pygame.draw.line(screen, white, [0,0], [319,0], 3)
# pygame.draw.line(screen, white, (319,0), (319,240), 3)
# pygame.draw.line(screen, white, (0,238), (320,238), 3)
# pygame.draw.line(screen, white, (0,0), (0,240), 3)

# pygame.draw.line(screen, white, (160,0), (160,240), 3)
# pygame.draw.line(screen, white, (0,120), (320,120), 3)

# pygame.display.flip()

def sound_alarm(sound_queue):
	# play an alarm sound
    while True:
        pass
        # time.sleep(0.2)
        # warning_message = sound_queue.get(block=True)
        # print(warning_message)
        # if "OFF_HAND" in warning_message.keys() and warning_message["OFF_HAND"]:
            # pygame.draw.rect(screen,red,(0,121,159,119))
            # screen.blit(wheel_alert, rect_wheel_alert)
        # else:
        #     pygame.draw.rect(screen,black,(0,121,159,119))
        # if "DROWSY" in warning_message.keys():
        #     if warning_message["DROWSY"] or warning_message["YAWN"]:
        #         os.system('espeak -ven+f2 -k5 -s150 --stdout  "Wake Up, please" | aplay ')
        #         pygame.draw.rect(screen,red,(0,0,159,119))
        #         screen.blit(drowsy_alert, rect_drowsy_alert)
        #     else:
        #         pygame.draw.rect(screen,black,(0,0,159,119))

        #     if warning_message["DISTRACTED"]:
        #         os.system('espeak -ven+f2 -k5 -s150 --stdout  "Focus on the road, please" | aplay ')
        #         pygame.draw.rect(screen,red,(161,0,159,119))
        #         screen.blit(distracted_alert, rect_distracted_alert)
        #     else:
        #         pygame.draw.rect(screen,black,(161,0,159,119))
        
        # pygame.display.flip()

 
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
    while True:
        image_queque.put(cap.read()[1])
        image_queque.get() if image_queque.qsize() > 1 else time.sleep(0.01)
        
def image_get(process_queue):
    while True:
        frame = process_queue.get()
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(5)&0xFF
	
	# # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        #  pass
    
    

# Facial processing
def facial_processing(image_queue, process_queue, sound_queue):
    distracton_initialized   = False
    eye_initialized          = False
    eye_tracking_initialized = False
    mouth_initialized        = False
	
    #get face detector and facial landmark predector
    detector    = dlib.get_frontal_face_detector()
    predictor   = dlib.shape_predictor(shape_predictor_path)

    drowsy = False
    yawn = False
    distracted = False
    # grab the indexes of the facial landmarks for the left and right eye, respectively
    ls,le = face.FACIAL_LANDMARKS_IDXS["left_eye"]
    rs,re = face.FACIAL_LANDMARKS_IDXS["right_eye"]
        
    # loop over frames from the video stream
    while True:
        # time.sleep(0.2)
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
                if not eye_initialized:
                    eye_start_time= time.time()
                    eye_initialized=True
		#checking if eyes are drowsy for a sufficient number of frames
                if time.time()-eye_start_time >= EYE_DROWSINESS_INTERVAL:
                    drowsy = True
                    cv2.putText(frame, "YOU ARE DROWSY!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
            else:
                drowsy = False
                    
        
            # #tracking the driver's eyes
            # #top_left     = [leftEye[0][0], leftEye[5][1]]
            # #top_right    = [leftEye[3][0], leftEye[5][1]]
            # #bottom_left  = [leftEye[0][0], leftEye[1][1]]
            # #bottom_right = [leftEye[3][0], leftEye[1][1]]
            x1 = leftEye[0][0]
            y1 = leftEye[5][1]
            
            x2 = leftEye[3][0]
            y2 = leftEye[1][1] 
            
            crop_frame = frame[y1:y2, x1:x2]
            cv2.imshow("Cropped", crop_frame)
            gray2 = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
            th_left = cv2.adaptiveThreshold(gray2, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 45)
            cnts, _ = cv2.findContours(th_left, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            cnt = max(cnts, key = cv2.contourArea)
            # calculate moments of binary image
            M = cv2.moments(th_left)
            # calculate x coordinate of center
            cX = int(M["m10"] / M["m00"])
            C = distance.euclidean(leftEye[0], leftEye[3])
            if cX < leftEye[0][0] + float(C)/4 or cX > leftEye[3][0] - float(C)/4:
                if not eye_tracking_initialized:
                    eye_tracking_start_time = time.time()
                    eye_tracking_initialized = True
                if time.time()-eye_tracking_start_time >= EYE_TRACKING_INTERVAL:
                    cv2.putText(frame,"YOU ARE NOT FOCUSED ON THE ROAD",(10,70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    sound_queue.put("LOOK AT THE ROAD")
                    sound_queue.get() if sound_queue.qsize() > 1 else time.sleep(0.01)
            
	    #checks if user is yawning
            if mar > MOUTH_DROWSINESS_THRESHOLD:
                if not mouth_initialized:
                    mouth_start_time= time.time()
                    mouth_initialized=True
		#checks if the user is yawning for a sufficient number of frames
                if time.time()-mouth_start_time >= MOUTH_DROWSINESS_INTERVAL:
                    yawn = True
                    cv2.putText(frame, "YOU ARE YAWNING!", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                yawn = False        
  
	#if the user's face is not focused on the road, the eyes/mouth features cannot be computed
        else:
            distracted = False
            if not distracton_initialized:
                distracton_start_time=time.time()
                distracton_initialized=True
	    #checks if the user's eyes are off the road after a sufficient number of frames
                if time.time()- distracton_start_time> DISTRACTION_INTERVAL and distracton_initialized:
            #displays on screen that the driver's eyes are off the road
                    distracted = True
                    cv2.putText(frame, "PLEASE KEEP EYES ON ROAD", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    time.sleep(3.1)
                    distracton_initialized= False
                

        # pass the frame to image_get
        process_queue.put(frame)
        process_queue.get() if process_queue.qsize() > 1 else time.sleep(0.01)
        message_dict = {"DROWSY": drowsy, "YAWN": yawn, "DISTRACTED":  distracted}
        print(message_dict)
        sound_queue.put(message_dict)
        sound_queue.get() if sound_queue.qsize() > 1 else time.sleep(0.01)
	

def wheel_detection(sound_queue):
    while True:
        value_list = [mpr121[0].value, mpr121[1].value, mpr121[2].value, mpr121[3].value]
        if any(value_list):
            # print('Detected')
            hand_off_alarm = False
        else:
            # print('Not detected')
            hand_off_alarm = True
        message_dict = {"OFF_HAND": hand_off_alarm} 
        
        sound_queue.put(message_dict)
        sound_queue.get() if sound_queue.qsize() > 1 else time.sleep(0.01)
    

if __name__=='__main__':
    
    image_queue = Queue()
    process_queue = Queue()
    sound_queue = Queue()
    process1 = Process(target=image_put, args=(image_queue,))
    process1.daemon = True
    process2 = Process(target=image_get, args=(process_queue,))
    process2.daemon = True
    process3 = Process(target=facial_processing, args=(image_queue, process_queue, sound_queue))
    process3.daemon = True
    process4 = Process(target=sound_alarm, args=(sound_queue,))
    process4.daemon = True
    process5 = Process(target=wheel_detection, args=(sound_queue,))
    process5.daemon = True
    process1.start()
    process2.start()
    process3.start()
    process4.start()
    process5.start()
    process1.join()
    process2.join()
    process3.join()
    process4.join()
    process5.join()
    print("End All Process!")
