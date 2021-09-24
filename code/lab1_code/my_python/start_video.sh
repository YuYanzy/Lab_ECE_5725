# !/bin/bash
# Yu Zhang yz2729
# Xinyu Wu xw586
# Lab 1  Date: 09/16/21
python3 /home/pi/lab1_files_f21/py_tests/my_python/video_control.py &
SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb1 mplayer -vo sdl -framedrop -input file=/home/pi/video_fifo /home/pi/bigbuckbunny320p.mp4

