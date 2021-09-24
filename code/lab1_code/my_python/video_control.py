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
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    time.sleep(0.2)
    if(not GPIO.input(17)):
        # Pause
        print("Button 17 has been pressed")
        cmd = 'echo "pause" > /home/pi/video_fifo'
        print("Pause the Video")
        os.system(cmd)
    elif( not GPIO.input(22)):
        # Fast Forward
        print("Button 22 has been pressed") 
        cmd = 'echo "seek 10 " > /home/pi/video_fifo'
        print("Fast forward 10 seconds")
        os.system(cmd)
    elif( not GPIO.input(23)):
        # Rewind
        print("Button 23 has been pressed")
        cmd = 'echo "seek -10" > /home/pi/video_fifo'
        print("Rewind 10 seconds")
        os.system(cmd)
    elif( not GPIO.input(27)):
        # Quit
        print("Button 27 has been pressed")
        cmd = 'echo "quit" > /home/pi/video_fifo'
        print("Quit the Video")
        os.system(cmd)
        break
