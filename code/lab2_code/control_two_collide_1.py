# M_ADL96_YZ483_Lab2
# Alex LoCicero (ADL96)
# Yingjie Zhao (YZ483)
# Sep 27, 2021
import RPi.GPIO as GPIO
import sys, os
import pygame
from pygame.locals import*
import time
keep_run = True             # Global variable used to track running status

# Button 27: quit
def GPIO27_callback(channel):
    print ("Button #27 pressed, quit.")
    global keep_run
    keep_run = False        # Set the keep_run flag to false in order to quit

def run():
    pygame.init()
    pygame.mouse.set_visible(True)
    WHITE = 255,255,255
    BLACK = 0,0,0
    size = width, height = 320, 240 #resolution of window
    screen = pygame.display.set_mode(size)
    my_font = pygame.font.Font(None, 20)
    start_btn = {'Start': (80,220)}
    start_rect = None
    quit_btn = {'Quit': (240,220)}
    quit_rect = None
    faster_btn = {'Faster': (40,220)}
    faster_rect = None
    slower_btn = {'Slower': (120,220)}
    slower_rect = None
    pause_btn = {'Pause': (200,220)}
    pause_rect = None
    back_btn = {'Back': (280,220)}
    back_rect = None
    playing = False                 # Menu level
    freeze = False                  # Pause flag

    # Two collide init
    speed1 = [1, 1]# speed of ball (pixels in x and y directions
    speed2 = [1, 1]# speed of ball (pixels in x and y directions
    ball1 = pygame.image.load("soccer-ball.png")
    ball2 = pygame.image.load("magic_ball.png")
    ball1 = pygame.transform.scale(ball1, (50, 50))
    ball2 = pygame.transform.scale(ball2, (50, 50))
    ballrect1 = ball1.get_rect()
    ballrect2 = ball2.get_rect()
    ballrect1.size=(40,40)
    ballrect2.size=(40,40)
    ballrect2.center = (280, 150)
    speed = 0.002                   # Speed control

    screen.fill(BLACK)
    global keep_run
    

    while keep_run:
        # Exit event detect
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.display.quit()
               keep_run = False

        # Blit button text
        if(playing):    # Menu level 2 (four buttons)
            for my_text, text_pos in faster_btn.items():    # Faster
                text_surface = my_font.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                faster_rect = rect
                screen.blit(text_surface, rect)

            for my_text, text_pos in slower_btn.items():    # Slower
                text_surface = my_font.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                slower_rect = rect
                screen.blit(text_surface, rect)

            for my_text, text_pos in pause_btn.items():     # Pause
                text_surface = my_font.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                pause_rect = rect
                screen.blit(text_surface, rect)

            for my_text, text_pos in back_btn.items():      # Back
                text_surface = my_font.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                back_rect = rect
                screen.blit(text_surface, rect)
        else:           # Menu level 1 (two buttons)
            for my_text, text_pos in start_btn.items():     # Start
                text_surface = my_font.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                start_rect = rect
                screen.blit(text_surface, rect)
            
            for my_text, text_pos in quit_btn.items():      # Quit
                text_surface = my_font.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                quit_rect = rect
                screen.blit(text_surface, rect)
        
        # Display Flip
        pygame.display.flip()

        # Touch detections
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
                if(playing):    # Menu level 2
                    if faster_rect.collidepoint(pos):   # Faster
                        print ("Faster button pressed")
                        if(speed > 0.0005):
                            speed -= 0.0002
                    elif slower_rect.collidepoint(pos): # Slower
                        print ("Slower button pressed")
                        if(speed < 0.05):
                            speed += 0.0002
                    elif pause_rect.collidepoint(pos):  # Pause
                        print ("Pause button pressed")
                        freeze = not freeze
                    elif back_rect.collidepoint(pos):   # Back
                        print ("Back button pressed")
                        playing = False
                        freeze = False
                else:           # Menu level 1
                    if quit_rect.collidepoint(pos):     # Quit
                        print ("Quit button pressed")
                        keep_run = False
                    elif start_rect.collidepoint(pos):  # Start
                        print ("Start button pressed")
                        playing = True
                        freeze = False
                    else:                               # Print screen coordinates
                        print(pos)
                        screen.fill(BLACK)
                        text_surface = my_font.render(("touch at "+str(pos)), True, WHITE)
                        rect = text_surface.get_rect(center=(160,120))
                        screen.blit(text_surface, rect)

            elif(event.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                x,y = pos

        # Refresh next screen
        screen.fill(BLACK)

        # Two collide animation
        if(playing):
            if(not freeze):
                ballrect1 = ballrect1.move(speed1)
                ballrect2 = ballrect2.move(speed2)

                # Collide detect
                collide = ballrect1.colliderect(ballrect2)
                if collide:
                    speed1[0] = -speed1[0]
                    speed1[1] = -speed1[1]
                    speed2[0] = -speed2[0]
                    speed2[1] = -speed2[1]

                # Edge detect
                if ballrect1.left < 0 or ballrect1.right > width:
                    speed1[0] = -speed1[0]
                if ballrect1.top < 0 or ballrect1.bottom > height-50:
                    speed1[1] = -speed1[1]

                if ballrect2.left < 0 or ballrect2.right > width:
                    speed2[0] = -speed2[0]
                if ballrect2.top < 0 or ballrect2.bottom > height-50:
                    speed2[1] = -speed2[1]
            screen.blit(ball1, ballrect1)
            screen.blit(ball2, ballrect2)
            time.sleep(speed)
    pygame.display.quit()       # Uninitialize the display module
    pygame.quit()               # Shutdown pygame

if __name__ == "__main__":
    os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
    os.putenv('SDL_FBDEV', '/dev/fb0') #
    os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)
   
    run()
    GPIO.cleanup()      # clean up GPIO on normal exit
