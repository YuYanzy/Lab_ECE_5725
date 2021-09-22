import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Add two more button 
GPIO.setup(NUMBER_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(NUMBER_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
    elif( not GPIO.input(NUMBER_1)):
        print("")
        print("Button NUMBER_1 has been pressed")
    elif( not GPIO.input(NUMBER_2)):
        print("")
        print("Button NUMBER_2 has been pressed")
    elif( not GPIO.input(27)):
        print("")
        print("Button 27 has been pressed")
        break
