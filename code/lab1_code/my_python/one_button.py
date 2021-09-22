import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)




while True:
    time.sleep(0.2)
    if(not GPIO.input(17)):
        print(" ")
        print("Button 17 has been pressed")
        
