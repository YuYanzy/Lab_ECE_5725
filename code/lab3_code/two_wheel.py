#! /usr/bin/python
import RPi.GPIO as GPIO

from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice

import time 

#setting the GPIO mode
GPIO.setmode(GPIO.BCM)

#setting up PWM
GPIO.setup(16, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#stopped to start
frequency = 1
servo_pin = GPIO.PWM(26, frequency)
servo2_pin = GPIO.PWM(16, frequency)
servo_pin.start(0)
servo2_pin.start(0)

left1_counter = 0
left2_flag = True

right1_counter = 0
right2_flag = True

def GPIO17_callback(channel):
    print("Button 17 has been pressed, start  or stop run the left wheel in clockwise\n")
    global left1_counter
    if left1_counter % 2 == 0:
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(6, GPIO.LOW)
        dutyCycle = 100
        servo_pin.ChangeDutyCycle(dutyCycle)
    elif left1_counter % 2 == 1:
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        dutyCycle = 0
        servo_pin.ChangeDutyCycle(dutyCycle)
    left1_counter += 1
    

def GPIO22_callback(channel):
    print("Button 22 has been pressed, change the direction for left wheel")
    global left2_flag 
    if left2_flag:
        left2_flag = False
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.HIGH)
    else:
        left2_flag = True
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(6, GPIO.LOW)

def GPIO23_callback(channel):
    print("Button 23 has been pressed, start  or stop run the right wheel\n")
    global right1_counter
    if right1_counter % 2 == 0:
        GPIO.output(19, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)
        dutyCycle = 100
        servo2_pin.ChangeDutyCycle(dutyCycle)
    elif right1_counter % 2 == 1:
        GPIO.output(19, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        dutyCycle = 0
        servo2_pin.ChangeDutyCycle(dutyCycle)
    right1_counter += 1
    
    

def GPIO27_callback(channel):
    print("Button 27 has been pressed, change the direction for right wheel\n")
    global right2_flag 
    if right2_flag:
        right2_flag = False
        GPIO.output(19, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
    else:
        right2_flag = True
        GPIO.output(19, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)
    


if __name__ == "__main__":
   
    GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
    GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
    GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
    GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)
    
    time.sleep(500)
    
    servo_pin.stop()
    servo2_pin.stop()
    GPIO.cleanup()


