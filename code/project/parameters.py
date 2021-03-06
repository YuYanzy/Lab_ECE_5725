import os

#change path to where you saved the shape predictor file
shape_predictor_path    = os.path.join('./', 'shape_predictor_68_face_landmarks.dat')

#feel free to customize these thresholds/intervals 

EYE_DROWSINESS_THRESHOLD    = 0.28
EYE_DROWSINESS_INTERVAL     = 2.0
MOUTH_DROWSINESS_THRESHOLD  = 0.3
MOUTH_DROWSINESS_INTERVAL   = 1.0
DISTRACTION_INTERVAL        = 3.0
NORMAL_INTERVAL             = 1.0
EYE_TRACKING_INTERVAL       = 8.0

