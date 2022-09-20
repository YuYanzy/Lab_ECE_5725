# Yu Zhang yz2729
# Lab 2  Date: 09/23/21
import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Add two more button 
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    time.sleep(0.2)
    if(not GPIO.input(17)):
        print(" ")
        print("Button 17 has been pressed")
    elif( not GPIO.input(22)):
        print("")
        print("Button 22 has been pressed")    
    elif( not GPIO.input(23)):
        print("")
        print("Button 23 has been pressed")
    elif( not GPIO.input(26)):
        print("")
        print("Button 26 has been pressed")
    elif( not GPIO.input(19)):
        print("")
        print("Button 19 has been pressed")
    elif( not GPIO.input(27)):
        print("")
        print("Button 27 has been pressed")
        break
