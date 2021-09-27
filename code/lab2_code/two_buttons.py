# Yu Zhang
# Monday Lab2
from pygame.locals import *
import RPi.GPIO as GPIO
import pygame
import time
import os
# Global Flag
CODERUN = True
START_GAME  = False
# Environment Seting
os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb0') #
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
# Init Pygame
pygame.init()
pygame.mouse.set_visible(False)
size = (width, height) = (320, 240)
screen = pygame.display.set_mode(size)
FPS = 40
clock = pygame.time.Clock()
WHITE = 255,255,255
BLACK = 0,0,0
screen.fill(BLACK)
# Button Configuration
button_font = pygame.font.Font(None, 30)
buttons_dic = {"Quit":(270, 220), "Start": (50,220)}
touch_info_font = pygame.font.Font(None, 30)
# Store pressed positions 
pressed_positions_list = []
# Ball Configuration
# Big Ball 
speed_big = [1,1] 
ball_big = pygame.image.load("magic_ball.png")
ballrect_big = ball_big.get_rect()
ballrect_big.center = (198,100)
ball_big_radius = 64

# Small Ball
speed_small = [-2,-2] 
ball_small = pygame.image.load("soccer-ball.png")
ballrect_small = ball_small.get_rect()
ballrect_small.center = (100,100)
ball_small_radius = 24

# GPIO Setting
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN,pull_up_down = GPIO.PUD_UP)    
def GPIO17_callback(channel):
    global CODERUN  
    print("Quit by Bail-out button!!!")
    CODERUN = False
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)

def check_start_button_press(position):
    x,y = position
    # Check if the touch position is in the button area
    if (y < 240 and y > 200) and (x < 80 and x > 20):
        global START_GAME
        START_GAME = True
        print("Start Game!!!")

def check_quit_button_press(position):
    x,y = position
    # Check if the touch position is in the button area
    if (y < 240 and y > 200) and (x < 290 and x > 240):
        global CODERUN
        CODERUN = False
        print("Qiut Game!!!")

def check_colliderect():
    dx = abs(ballrect_big.centerx - ballrect_small.centerx)
    dy = abs(ballrect_big.centery - ballrect_small.centery)
    if( dx < (ball_big_radius + ball_small_radius - 30) and dy < (ball_big_radius + ball_small_radius - 25)):
        return True
    else:
        return False

def check_run_game():
    if (START_GAME):
        global ballrect_big, ballrect_small
        ballrect_big = ballrect_big.move(speed_big)    
        if ballrect_big.left < 0 or ballrect_big.right > width:        
            speed_big[0] = -speed_big[0]    
        if ballrect_big.top < 0 or ballrect_big.bottom > 200:        
            speed_big[1] = -speed_big[1]

        ballrect_small= ballrect_small.move(speed_small)    
        if ballrect_small.left < 0 or ballrect_small.right > width:        
            speed_small[0] = -speed_small[0]    
        if ballrect_small.top < 0 or ballrect_small.bottom > 200:        
            speed_small[1] = -speed_small[1]

        if check_colliderect():
            speed_big[0] = - speed_big[0]
            speed_big[1] = - speed_big[1]
            speed_small[0] = - speed_small[0]
            speed_small[1] = - speed_small[1]

def refresh_touch_info(position):
    x, y = position
    touch_position_info = "touch at " + str(x) + ", " + str(y)
    touch_info_text_surface = touch_info_font.render(touch_position_info, True, WHITE)
    touch_info_rect = touch_info_text_surface.get_rect(center=(160,220))
    screen.blit(touch_info_text_surface, touch_info_rect)

def refresh_game(touch_position):
    # print("Refresh the Game")
    screen.fill(BLACK)
    # Draw Buttons
    for text, center in buttons_dic.items():
        text_surface = button_font.render(text , True, WHITE)
        # print(text_surface.get_width())
        # print(text_surface.get_height())
        rect = text_surface.get_rect(center=center)
        screen.blit(text_surface, rect)
    # Draw Ball
    screen.blit(ball_big, ballrect_big)
    screen.blit(ball_small, ballrect_small)
    # screen.blit(touch_info_text_surface, touch_info_rect)
    if (touch_position is not None):
        refresh_touch_info(touch_position)
    elif(len(pressed_positions_list) > 0):
        refresh_touch_info(pressed_positions_list[-1])
    else:
        touch_info_text_surface = touch_info_font.render('touch at ', True, WHITE)
        touch_info_rect = touch_info_text_surface.get_rect(center=(160,220))
        screen.blit(touch_info_text_surface, touch_info_rect)
    pygame.display.flip()

if __name__ == "__main__":
    screen.fill(BLACK)
    # Draw Buttons
    for text, center in buttons_dic.items():
        text_surface = button_font.render(text , True, WHITE)
        # print(text_surface.get_width())
        # print(text_surface.get_height())
        rect = text_surface.get_rect(center=center)
        screen.blit(text_surface, rect)
    # Draw the touch info
    touch_info_text_surface = touch_info_font.render('touch at ', True, WHITE)
    touch_info_rect = touch_info_text_surface.get_rect(center=(160,220))
    # Draw Ball
    screen.blit(ball_big, ballrect_big)
    screen.blit(ball_small, ballrect_small) 
    screen.blit(touch_info_text_surface, touch_info_rect)
    pygame.display.flip()
   
    start_time = time.time()
    while (time.time() - start_time <= 360) and CODERUN:  
        clock.tick(FPS)
        touch_position = None
    	for event in pygame.event.get(): 
            if(event.type is MOUSEBUTTONDOWN): 
                # touch_position = pygame.mouse.get_pos()
                # print(touch_position)
                pass
            #on mouse press
            elif(event.type is MOUSEBUTTONUP):
                touch_position = pygame.mouse.get_pos()
                print(touch_position)
                pressed_positions_list.append(touch_position)
                check_start_button_press(touch_position)
                check_quit_button_press(touch_position)
        check_run_game()
        # refresh
        refresh_game(touch_position)
