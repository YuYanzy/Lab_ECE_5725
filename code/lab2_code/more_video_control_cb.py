import RPi.GPIO as GPIO
import os
import time

CODERUN = True
def GPIO17_callback(channel):
    print("Button 17 has been pressed")
    cmd = 'echo "pause" > /home/pi/video_fifo'
    print("Pause the Video")
    os.system(cmd)

def GPIO22_callback(channel):
    print("Button 22 has been pressed") 
    cmd = 'echo "seek 10 " > /home/pi/video_fifo'
    print("Fast forward 10 seconds")
    os.system(cmd)

def GPIO23_callback(channel):
    print("Button 23 has been pressed")
    cmd = 'echo "seek -10" > /home/pi/video_fifo'
    print("Rewind 10 seconds")
    os.system(cmd)

def GPIO_26_callback(channel):
    print("Button 26 has been pressed") 
    cmd = 'echo "seek 30 " > /home/pi/video_fifo'
    print("Fast forward 30 seconds")
    os.system(cmd)

def GPIO_19_callback(channel):
    print("Button 19 has been pressed")
    cmd = 'echo "seek -30" > /home/pi/video_fifo'
    print("Rewind 30 seconds")
    os.system(cmd)

def GPIO27_callback(channel):
    print("Button 27 has been pressed")
    cmd = 'echo "quit" > /home/pi/video_fifo'
    print("Quit the Video")
    os.system(cmd)
    global CODERUN
    CODERUN = False

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if __name__ == '__main__':
    GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=500)
    GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=500)
    GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=500)
    GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=500)
    GPIO.add_event_detect(26,GPIO.FALLING, callback=GPIO_26_callback, bouncetime=500)
    GPIO.add_event_detect(19,GPIO.FALLING, callback=GPIO_19_callback, bouncetime=500)
    time.sleep(120)
    GPIO.cleanup()