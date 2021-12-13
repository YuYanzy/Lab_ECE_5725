from pygame.locals import *
import os
import pygame
import sys
import time
# import RPi.GPIO as GPIO

# set up the enviroments
# os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
# os.putenv('SDL_FBDEV', '/dev/fb1')
# os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
# os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


CODERUN = True

#setting the GPIO mode
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)


speed_file = open('speed_log.txt', 'r')


# def GPIO27_callback(channel):
#     global CODERUN
#     print("Button 27 has been pressed, quit the pygame_interface program\n")
#     CODERUN = False
#     GPIO.cleanup()
#     pygame.display.quit()
#     pygame.quit()
#     speed_file.close()
#     sys.exit(0)
    
    
pygame.init()
size = (width, height) = (320, 240)
screen = pygame.display.set_mode(size)
my_font = pygame.font.Font(None,26)
white = 255,255,255
black = 0,0,0
green = 0,255,0
red = 255,0,0


drowsy_alert = my_font.render("Drowsy", True, white)
rect_drowsy_alert = drowsy_alert.get_rect(center = (80,90))
distracted_alert = my_font.render("Looking Away", True, white)
rect_distracted_alert = distracted_alert.get_rect(center = (240,90))
yawn_alert = my_font.render("Yawn", True, white)
rect_yawn_alert = yawn_alert.get_rect(center = (80, 190))
wheel_alert = my_font.render("Wheel", True, white)
rect_wheel_alert = wheel_alert.get_rect(center = (240,190))

drowsy_counter = 0
distracted_counter = 0
yawn_counter = 0
wheel_counter = 0

speed_info = "Can not detecting the speed"
info_font = pygame.font.Font(None,20)

def draw_interface():
    global speed_info, drowsy_counter, distracted_counter, yawn_counter, wheel_counter
    speed_surface = info_font.render(speed_info,False,white)
    screen.blit(speed_surface,(100,20))
    drowsy_counter_surface = info_font.render("Drowsy: " + str(drowsy_counter),False,white)
    screen.blit(drowsy_counter_surface,(90,120))
    distracted_counter_surface = info_font.render("Distracted: " + str(distracted_counter),False,white)
    screen.blit(distracted_counter_surface,(230,120))
    yawn_counter_surface = info_font.render("Yawn: " + str(yawn_counter),False,white)
    screen.blit(yawn_counter_surface,(100,220))
    wheel_counter_surface = info_font.render("Wheel: " + str(wheel_counter),False,white)
    screen.blit(wheel_counter_surface,(255,220))
    
    pygame.draw.line(screen, white, [0,0], [320,0], 3)
    pygame.draw.line(screen, white, (320,0), (320,240), 3)
    pygame.draw.line(screen, white, (0,240), (320,240), 3)
    pygame.draw.line(screen, white, (0,0), (0,240), 3)
    
    pygame.draw.line(screen, white, [0, 40], [320, 40], 3)
    pygame.draw.line(screen, white, [0, 140], [320, 140], 3)
    pygame.draw.line(screen, white, [160, 40], [160, 240], 3)
    pygame.display.flip()


def update_interface():
    global CODERUN
    global speed_info, drowsy_counter, distracted_counter, yawn_counter, wheel_counter
    while CODERUN:
        time.sleep(0.1)
        screen.fill(black)
        current_line = speed_file.readline()
        print(current_line)
        current_speed = 0
        if current_line != "":
            current_speed = float(current_line.split( )[1])
            current_speed = round(current_speed,2)
            speed_info = "Current speed: " + str(current_speed) + " mph"
        f = open('message.txt', 'r')
        lines = f.readlines()
        if current_speed > 0:
            if len(lines) > 0:
                last_line = lines[-1]
                print(last_line) 
                cmd = ""
                # First Quadrant
                if last_line == "DROWSY\n":
                    drowsy_counter += 1
                    pygame.draw.rect(screen,red,(0,40,80,50))
                    screen.blit(drowsy_alert, rect_drowsy_alert)
                    cmd = 'espeak -ven+f2 -k5 -s150 --stdout  "Drowsing" | aplay '
                    
                if last_line == "NOT_DROWSY\n":
                    pygame.draw.rect(screen,black,(0,40,80,50))
                
                # Second Quadrant
                if last_line == "EYE_OFF_ROAD\n":
                    distracted_counter += 1
                    pygame.draw.rect(screen,red,(160,40,80,50))
                    screen.blit(distracted_alert, rect_distracted_alert)
                    pygame.draw.rect(screen,black,(0,40,80,50))
                    pygame.draw.rect(screen,black,(0,140,80,50))
                    cmd = 'espeak -ven+f2 -k5 -s150 --stdout  "Distracted" | aplay '
                if last_line == "EYE_ON_ROAD\n":
                    pygame.draw.rect(screen,black,(160,40,80,50))

                # Third Quadrant
                if last_line == "YAWN\n":
                    yawn_counter += 1
                    pygame.draw.rect(screen,red,(0,140,80,50))
                    screen.blit(yawn_alert, rect_yawn_alert)
                    cmd = 'espeak -ven+f2 -k5 -s150 --stdout  "Yawning" | aplay '
                if last_line == "NOT_YAWN\n":
                    pygame.draw.rect(screen,black,(0,140,80,50))
                
                # Last Quadrant
                if last_line == "HAND_OFF_WHEEL\n":
                    wheel_counter += 1
                    pygame.draw.rect(screen,red,(160, 90,80,50))
                    screen.blit(wheel_alert,rect_wheel_alert)
                    cmd = 'espeak -ven+f2 -k5 -s150 --stdout  "Hand off Wheel" | aplay '
                if last_line == "HAND_ON_WHEEL\n":
                    pygame.draw.rect(screen,black,(160, 90,80,50))
                
                if cmd != "":
                    os.system(cmd)
            
        # else:
        #     screen.fill(black)
        f.close()
        w = open('message.txt', 'w')
        w.close()  
        draw_interface()  
        
    

if __name__ == "__main__":
    # GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=500)
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
    