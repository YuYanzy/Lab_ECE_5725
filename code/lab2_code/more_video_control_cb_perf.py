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

def GPIO_NUMBER_1_callback(channel):
    print("Button NUMBER_1 has been pressed") 
    cmd = 'echo "seek 30 " > /home/pi/video_fifo'
    print("Fast forward 30 seconds")
    os.system(cmd)

def GPIO_NUMBER_2_callback(channel):
    print("Button NUMBER_2 has been pressed")
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
GPIO.setup(NUMBER_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(NUMBER_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)
GPIO.add_event_detect(NUMBER_1,GPIO.FALLING, callback=GPIO_NUMBER_1_callback, bouncetime=300)
GPIO.add_event_detect(NUMBER_2,GPIO.FALLING, callback=GPIO_NUMBER_2_callback, bouncetime=300)

print("Waiting for button press")
start_time = time.time()
try:
    while (time.time() - start_time <= 10) :
        pass
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()