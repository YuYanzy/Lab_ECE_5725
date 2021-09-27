import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    time.sleep(0.2)
    if(not GPIO.input(17)):
        print(" ")
        print("Button 17 has been pressed")
        cmd = 'echo "pause" > /home/pi/video_fifo1'
        print("Pause the Video")
        os.system(cmd)
    elif( not GPIO.input(22)):
        print("")
        print("Button 22 has been pressed") 
        cmd = 'echo "seek 10 " > /home/pi/video_fifo1'
        print("Fast forward 10 seconds")
        os.system(cmd)
    elif( not GPIO.input(23)):
        print("")
        print("Button 23 has been pressed")
        cmd = 'echo "seek -10" > /home/pi/video_fifo1'
        print("Rewind 10 seconds")
        os.system(cmd)
    elif( not GPIO.input(27)):
        print("")
        print("Button 27 has been pressed")
        cmd = 'echo "quit" > /home/pi/video_fifo1'
        print("Quit the Video")
        os.system(cmd)
        break
