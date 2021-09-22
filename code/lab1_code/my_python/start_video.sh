# !/bin/bash
#
#

python3 /home/pi/lab1_files_f21/py_tests/my_python/video_control.py &
SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb1 mplayer -vo sdl -framedrop -input file=/home/pi/video_fifo /home/pi/bigbuckbunny320p.mp4 

