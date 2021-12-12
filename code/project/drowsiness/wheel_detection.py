import time
import board
import busio
import adafruit_mpr121
import os
import sys
import RPi.GPIO as GPIO
from threading import Thread


i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

alarm = False
interval = 5
counter = 0

CODERUN = True

#setting the GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def GPIO27_callback(channel):
    global CODERUN
    print("Button 27 has been pressed, quit the wheel_detection program\n")
    CODERUN = False
    GPIO.cleanup()
    f.close()
    sys.exit(0)
    
def sound_alarm():
    os.system('espeak -ven+f2 -k5 -s150 --stdout  "Hands off wheel" | aplay ')

if __name__=='__main__':
    GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=500)
    try:
        while CODERUN:
            time.sleep(0.25)
            value_list = [mpr121[0].value, mpr121[1].value, mpr121[2].value, mpr121[3].value]
            f = open('message.txt', 'a+')
            # print(counter)
            if any(value_list):
                print("Detected")
                if alarm:
                    alarm = False
                    counter = 0
                    print('Detected Again')
                    f.write("HAND_ON_WHEEL\n")
            else:
                counter += 1
                if counter >= 15:
                    alarm = True
                    print('Not detected')
                    f.write("HAND_OFF_WHEEL\n")
                    counter = 0
                    # t = Thread(target=sound_alarm)
                    # t.deamon = True
                    # t.start()
                    # t.join()
            f.close()
                    
                    
    except KeyboardInterrupt:
        try:
            print(" Exit wheel detection!")
            sys.exit(0)
        except SystemExit:
            # print("Somthing Wrong, clean every thing and exit!")
            GPIO.cleanup()
            f.close()
            os._exit(0)

