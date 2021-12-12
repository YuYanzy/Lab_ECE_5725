from pygame.locals import *
import os
import pygame
import sys
import time
import RPi.GPIO as GPIO

# set up the enviroments
# os.putenv('SDL_VIDEODRIVER', 'x11') # Display on piTFT
# os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
# os.putenv('SDL_FBDEV', '/dev/fb1')
# os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
# os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


CODERUN = True

#setting the GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)


speed_file = open('speed_log.txt', 'r')


def GPIO27_callback(channel):
    global CODERUN
    print("Button 27 has been pressed, quit the pygame_interface program\n")
    CODERUN = False
    GPIO.cleanup()
    pygame.display.quit()
    pygame.quit()
    speed_file.close()
    sys.exit(0)
    
    
pygame.init()
# screen = pygame.display.set_mode((800,600))
size = (width, height) = (600, 800)
screen = pygame.display.set_mode(size)
my_font = pygame.font.Font(None,26)
white = 255,255,255
black = 0,0,0
green = 0,255,0
red = 255,0,0


drowsy_alert = my_font.render("Drowsy", True, white)
rect_drowsy_alert = drowsy_alert.get_rect(center = (150,350))
distracted_alert = my_font.render("Looking Away", True, white)
rect_distracted_alert = distracted_alert.get_rect(center = (450,350))
yawn_alert = my_font.render("Yawn", True, white)
rect_yawn_alert = yawn_alert.get_rect(center = (150, 650))
wheel_alert = my_font.render("Wheel", True, white)
rect_wheel_alert = wheel_alert.get_rect(center = (450,650))


def draw_interface():

    # pygame.draw.line(screen, white, [0,0], [319,0], 3)
    # pygame.draw.line(screen, white, (319,0), (319,240), 3)
    # pygame.draw.line(screen, white, (0,238), (320,238), 3)
    # pygame.draw.line(screen, white, (0,0), (0,240), 3)

    # pygame.draw.line(screen, white, (160,0), (160,240), 3)
    # pygame.draw.line(screen, white, (0,120), (320,120), 3)
    
    pygame.draw.line(screen, white, [0, 200], [600, 200], 3)
    pygame.draw.line(screen, white, [0, 500], [600, 500], 3)
    pygame.draw.line(screen, white, [300, 200], [300, 800], 3)
    pygame.display.flip()


def update_interface():
    global CODERUN

    while CODERUN:
        # time.sleep(0.25)
        current_line = speed_file.readline()
        print(current_line)
        current_speed = 0
        if current_line != "":
            current_speed = float(current_line.split( )[1])
        f = open('message.txt', 'r')
        lines = f.readlines()
        if current_speed > 0:
            if len(lines) > 0:
                last_line = lines[-1]
                print(last_line)
                cmd = ""
                # First Quadrant
                if last_line == "DROWSY\n":
                    pygame.draw.rect(screen,red,(0,200,300,300))
                    screen.blit(drowsy_alert, rect_drowsy_alert)
                    cmd = 'espeak -ven+f2 -k5 -s150 --stdout  "Drowsing" | aplay '
                    
                if last_line == "NOT_DROWSY\n":
                    pygame.draw.rect(screen,black,(0,200,300,300))
                
                # Second Quadrant
                if last_line == "EYE_OFF_ROAD\n":
                    pygame.draw.rect(screen,red,(300,200,300,300))
                    screen.blit(distracted_alert, rect_distracted_alert)
                    pygame.draw.rect(screen,black,(0,200,300,300))
                    pygame.draw.rect(screen,black,(0,500,300,300))
                    cmd = 'espeak -ven+f2 -k5 -s150 --stdout  "Distracted" | aplay '
                if last_line == "EYE_ON_ROAD\n":
                    pygame.draw.rect(screen,black,(300,200,300,300))

                # Third Quadrant
                if last_line == "YAWN\n":
                    pygame.draw.rect(screen,red,(0,500,300,300))
                    screen.blit(yawn_alert, rect_yawn_alert)
                    cmd = 'espeak -ven+f2 -k5 -s150 --stdout  "Yawning" | aplay '
                if last_line == "NOT_YAWN\n":
                    pygame.draw.rect(screen,black,(0,500,300,300))
                
                # Last Quadrant
                if last_line == "HAND_OFF_WHEEL\n":
                    pygame.draw.rect(screen,red,(300,500,300,300))
                    screen.blit(wheel_alert,rect_wheel_alert)
                    cmd = 'espeak -ven+f2 -k5 -s150 --stdout  "Hand off Wheel" | aplay '
                if last_line == "HAND_ON_WHEEL\n":
                    pygame.draw.rect(screen,black,(300,500,300,300))
                
                if cmd != "":
                    os.system(cmd)
            
        else:
            screen.fill(black)
        f.close()
        w = open('message.txt', 'w')
        w.close()  
        draw_interface()  
        
    

if __name__ == "__main__":
    GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=500)
    draw_interface()
    txt_file = open('message.txt', 'w')
    txt_file.close()
    try:
        # draw_interface()
        update_interface()
    
    except KeyboardInterrupt:
        try:
            print("Exit PyGame")
            pygame.display.quit()
            pygame.quit()
            sys.exit(0)
        except SystemExit:
            pygame.display.quit()
            pygame.quit()
            os._exit(0)
    