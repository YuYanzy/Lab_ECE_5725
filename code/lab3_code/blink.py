#! /usr/bin/python
import RPi.GPIO as GPIO

import time 

#setting up gpio pin for pwm
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
led_pin = GPIO.PWM(26, 1)
led_pin.start(50)

#taking user input to change the frequency of the PWM signal
while(1):
    usr_in = 1
    usr_in = input("Enter a Frequency:")
    led_pin.ChangeFrequency(int(usr_in))
    time.sleep(0.5)
