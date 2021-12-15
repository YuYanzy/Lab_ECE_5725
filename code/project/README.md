# Connect OBD
mac_address: 00:1D:A5:23:15:51 
sudo rfcomm bind /dev/rfcomm0 00:1D:A5:23:15:51

# Pygame_interface
```
ssh -X pi@ip_address
cd /home/pi/Lab_ECE_5725/code/project/drowsiness
export XAUTHORITY=$HOME/.Xauthority
sudo python3 pygame_interface.py
```

# wheel_detection.py
```
cd /home/pi/Lab_ECE_5725/code/project/drowsiness
python3 wheel_detection.py
```

# face_process.py
```
cd /home/pi/Lab_ECE_5725/code/project/drowsiness
python3 face_process.py
```

GPIO 27 for quiting all programs