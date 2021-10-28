# Yu Zhang yz2729
# Lab 3  Date: 10/04/21
import RPi.GPIO as GPIO
import time 
#setting up gpio pin for pwm
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
led_pin = GPIO.PWM(26, 1)
led_pin.start(50)

#taking user input to change the frequency of the PWM signal
while(1):
    usr_in = 1
    usr_in = input("Enter a Frequency:")
    led_pin.ChangeFrequency(int(usr_in))
    time.sleep(0.5)
