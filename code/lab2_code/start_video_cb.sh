# !/bin/bash
#
#

python3 /home/pi/Lab_ECE_5725/code/lab2_code/more_video_control_cb.py &
SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb1 mplayer -vo sdl -framedrop -input file=/home/pi/video_fifo /home/pi/bigbuckbunny320p.mp4 

