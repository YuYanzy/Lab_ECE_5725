# Yu Zhang yz2729
# Xinyu Wu xw586
# Lab 1  Date: 09/16/21
import subprocess
import os
while True:
    # Get inpu from the user
    command = input("Please input a command: ")
    print(command)
    if command == "pause":
        # Pause
        cmd = 'echo "pause" > /home/pi/video_fifo'
        os.system(cmd)
    elif command == "get_file_name":
        # Get File Name
        cmd = 'echo "get_file_name" > /home/pi/video_fifo'
        os.system(cmd)
    elif command == "speed_set":
        # Speed Up
        cmd = 'echo "speed_set 10" > /home/pi/video_fifo'
        os.system(cmd)
    elif command == "quit":
        # Quit
        cmd = 'echo "quit" > /home/pi/video_fifo'
        os.system(cmd)
        break
print("The viedo is end!")
