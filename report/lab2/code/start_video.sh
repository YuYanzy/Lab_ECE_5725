# Yu Zhang yz2729
# Lab 2  Date: 09/23/21
# !/bin/bash

python3 /home/pi/Lab_ECE_5725/code/lab2_code/video_control.py &
SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb0 mplayer -vo sdl -framedrop -input file=/home/pi/video_fifo1 /home/pi/bigbuckbunny320p.mp4 

