# Yu Zhang yz2729
# Xinyu Wu xw586
# Lab 1  Date: 09/16/21
import RPi.GPIO as GPIO
import os
import time
# Set Numbering System to BCM mode
GPIO.setmode(GPIO.BCM)
# Setup the GPIO channel
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    time.sleep(0.2)
    # Detect input
    if(not GPIO.input(17)):
        print("Button 17 has been pressed")
        
