import subprocess
import os



while True:
    command = input("Please input a command: ")
    print(command)
    if command == "pause":
        cmd = 'echo "pause" > /home/pi/video_fifo'
        os.system(cmd)
    elif command == "get_file_name":
        cmd = 'echo "get_file_name" > /home/pi/video_fifo'
        os.system(cmd)
    elif command == "speed_set":
        cmd = 'echo "speed_set 10" > /home/pi/video_fifo'
        os.system(cmd)
    elif command == "quit":
        cmd = 'echo "quit" > /home/pi/video_fifo'
        os.system(cmd)
        break
print("The viedo is end!")
