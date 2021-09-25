import RPi.GPIO as GPIO
import pygame     # Import pygame graphics library
import time
import os    # for OS calls


CODERUN = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN,pull_up_down = GPIO.PUD_UP)    
def GPIO17_callback(channel):
    global CODERUN  
    CODERUN = False
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)

# Environment Setting 
os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb0')   
pygame.init()

# Screen Setting
size = (width, height) = (320, 240)
# size = (width, height) = (800, 800) 
screen = pygame.display.set_mode(size)
black = 0, 0, 0
FPS = 40
clock = pygame.time.Clock()

# Big Ball 
speed_big = [1,1] 
ball_big = pygame.image.load("magic_ball.png")
ballrect_big = ball_big.get_rect()
ballrect_big.left = 192
ballrect_big.bottom = 128

# Small Ball
speed_small = [-2,-2] 
ball_small = pygame.image.load("soccer-ball.png")
ballrect_small = ball_small.get_rect()
ballrect_small.right = 50
ballrect_small.bottom = 240

start_time = time.time()
while (time.time() - start_time <= 360) and CODERUN:  
    # time.sleep(0.02)  
    clock.tick(FPS)
    ballrect_big = ballrect_big.move(speed_big)    
    if ballrect_big.left < 0 or ballrect_big.right > width:        
        speed_big[0] = -speed_big[0]    
    if ballrect_big.top < 0 or ballrect_big.bottom > height:        
        speed_big[1] = -speed_big[1]

    ballrect_small= ballrect_small.move(speed_small)    
    if ballrect_small.left < 0 or ballrect_small.right > width:        
        speed_small[0] = -speed_small[0]    
    if ballrect_small.top < 0 or ballrect_small.bottom > height:        
        speed_small[1] = -speed_small[1]

    if ballrect_big.colliderect(ballrect_small):
        # tmp = speed_big
        speed_big[0] = - speed_big[0]
        speed_big[1] = - speed_big[1]
        speed_small[0] = - speed_small[0]
        speed_small[1] = - speed_small[1]
    
    screen.fill(black)            # Erase the Work space
    screen.blit(ball_big, ballrect_big)   # Combine Ball surface with workspace surface
    screen.blit(ball_small, ballrect_small) 
    pygame.display.flip()         # display workspace on screen

GPIO.cleanup()