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
distracted_alert = my_font.render("Gaze Away", True, white)
rect_distracted_alert = distracted_alert.get_rect(center = (240,90))
head_alert = my_font.render("Head", True, white)
rect_head_alert = head_alert.get_rect(center = (80, 190))
wheel_alert = my_font.render("Wheel", True, white)
rect_wheel_alert = wheel_alert.get_rect(center = (240,190))


drowsy = False
distracted = False
head_off = False
wheel_off = False

drowsy_counter = 0
distracted_counter = 0
head_counter = 0
wheel_counter = 0

speed_info = "Can not detecting the speed"
info_font = pygame.font.Font(None,20)

def draw_interface():
    global speed_info, drowsy_counter, distracted_counter, head_counter, wheel_counter
    
    screen.fill(black)
    
    
    if drowsy:
        pygame.draw.rect(screen,red,(0,40,160,100))
        screen.blit(drowsy_alert, rect_drowsy_alert)
    else:
        pygame.draw.rect(screen,black,(0,40,160,100))
        
    if distracted:
        pygame.draw.rect(screen, red,(160,40,160,100))
        screen.blit(distracted_alert, rect_distracted_alert)
        pygame.draw.rect(screen, black,(0,40,160,100))
    else:
        pygame.draw.rect(screen, black,(160,40,160,100))
    
    if head_off:
        pygame.draw.rect(screen,red,(0,140,160,100))
        screen.blit(head_alert, rect_head_alert)
        pygame.draw.rect(screen,black,(0,40,160,100))
        pygame.draw.rect(screen,black,(160,40,160,100))
    else:
        pygame.draw.rect(screen,black,(0,140,160,100))
    
    if wheel_off:
        pygame.draw.rect(screen,red,(160, 140,160,100))
        screen.blit(wheel_alert,rect_wheel_alert)
    else:
        pygame.draw.rect(screen,black,(160, 140,160,100))
    
    speed_surface = info_font.render(speed_info,False,white)
    screen.blit(speed_surface,(100,20))
    drowsy_counter_surface = info_font.render("Drowsy: " + str(drowsy_counter),False,white)
    screen.blit(drowsy_counter_surface,(90,120))
    distracted_counter_surface = info_font.render("Gaze away: " + str(distracted_counter),False,white)
    screen.blit(distracted_counter_surface,(230,120))
    head_counter_surface = info_font.render("Face away: " + str(head_counter),False,white)
    screen.blit(head_counter_surface,(70,220))
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
    global speed_info, drowsy_counter, distracted_counter, head_counter, wheel_counter
    global drowsy, distracted, head_off, wheel_off
    while CODERUN:
        # time.sleep(0.1)
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
                    drowsy  = True
                    cmd = 'espeak -ven+f2 -k5 -s150 --stdout  "Drowsy" | aplay '
                    
                if last_line == "NOT_DROWSY\n":
                    drowsy = False
                
                # Second Quadrant
                if last_line == "EYE_OFF_ROAD\n":
                    distracted_counter += 1
                    distracted = True
                    drowsy = False
                    cmd = 'espeak -ven+f2 -k5 -s150 --stdout  "Eye" | aplay '

                if last_line == "EYE_ON_ROAD\n":
                    distracted = False

                # # Third Quadrant
                # if last_line == "head\n":
                #     head_counter += 1
                #     pygame.draw.rect(screen,red,(0,140,80,50))
                #     screen.blit(head_alert, rect_head_alert)
                #     cmd = 'espeak -ven+f2 -k5 -s150 --stdout  "heading" | aplay '
                # if last_line == "NOT_head\n":
                #     pygame.draw.rect(screen,black,(0,140,80,50))
                
                # Third Quadrant
                if last_line == "HEAD_OFF_ROAD\n":
                    head_counter += 1
                    head_off = True
                    drowsy  = False
                    distracted = False
                    cmd = 'espeak -ven+f2 -k5 -s150 --stdout  "Head" | aplay '
                if last_line == "HEAD_ON_ROAD\n":
                    head_off = False
                
                # Last Quadrant
                if last_line == "HAND_OFF_WHEEL\n":
                    wheel_counter += 1
                    wheel_off = True
                    cmd = 'espeak -ven+f2 -k5 -s150 --stdout  "Wheel" | aplay '

                if last_line == "HAND_ON_WHEEL\n":
                    wheel_off = False
                
                if cmd != "":
                    os.system(cmd)
        else:
            drowsy = False
            distracted = False
            head_off = False
            wheel_off = False
                
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
    