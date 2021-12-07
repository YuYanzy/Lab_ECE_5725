import time
import board
import busio
import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

alarm = False
speed = 1

def check_wheel():
    value_list = [mpr121[0].value, mpr121[1].value, mpr121[2].value, mpr121[3].value]

    if any(value_list):
        print('Detected')
        alarm = False
    else:
        if speed == 0:
            print('Not detected and STOPPED')
            alarm = False
        else:
            print('Not detected')
            alarm = True

while True:
    check_wheel()
    time.sleep(0.25)