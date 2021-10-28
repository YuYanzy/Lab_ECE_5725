# Yu Zhang yz2729
# Lab 3  Date: 10/04/21
import RPi.GPIO as GPIO
import time 

#setting the GPIO mode
GPIO.setmode(GPIO.BCM)

#setting the high duration for each stop in frequency/duty cycle
speed_dic= {"stop": 0, "half": 50, "full": 100}
#setting up PWM
GPIO.setup(26, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
#stopped to start
if __name__ == "__main__":
    print("Start at stop\n")
    frequency = 1
    servo_pin = GPIO.PWM(26, 1)
    servo_pin.start(0)
    time.sleep(2)
    print("Clockwise\n")
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(6, GPIO.LOW)
    for key,val in speed_dic.items():
        dutyCycle = 1 * val
        frequency += val
        print("Current Speed is: ", key, " current duty cycle is:", dutyCycle, " current frequency is:", frequency)
        servo_pin.ChangeDutyCycle(dutyCycle)
        servo_pin.ChangeFrequency(frequency)
        time.sleep(3)
    print("Clockwise End\n")
    servo_pin.stop()
    frequency = 1
    servo_pin = GPIO.PWM(26, 1)
    servo_pin.start(0)
    time.sleep(2)
    print("Counterclockwise\n")
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.HIGH)
    for key,val in speed_dic.items():
        dutyCycle = 1 * val
        frequency += val
        print("Current Speed is: ", key, " current duty cycle is:", dutyCycle, " current frequency is:", frequency)
        servo_pin.ChangeDutyCycle(dutyCycle)
        servo_pin.ChangeFrequency(frequency)
        time.sleep(3)
    servo_pin.stop()
    print("Counterclockwise End\n")
    GPIO.cleanup()




