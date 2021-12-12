import os
import sys
import time

f = open("speed.txt", "w")
f.close()

f = open("speed.txt", 'a+')


while True:
    time.sleep(1)
    speed = 0.0
    str = f'SPEED: {speed} mph\n'
    f.write(str)
    
