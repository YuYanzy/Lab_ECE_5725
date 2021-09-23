import pygame     # Import pygame graphics library
import os    # for OS calls
import time

# Environment Setting 
os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')   
pygame.init()

# Screen Setting
size = (width, height) = (320, 240) 
# size = (width, height) = (800, 800) 
screen = pygame.display.set_mode(size)
black = 0, 0, 0

# Big Ball 
speed_big = [1,1] 
ball_big = pygame.image.load("magic_ball.png")
ballrect_big = ball_big.get_rect()
ballrect_big.left = 192
ballrect_big.bottom = 128


start_time = time.time()
while time.time() - start_time <= 360:  
    time.sleep(0.02)  
    ballrect_big = ballrect_big.move(speed_big)    
    if ballrect_big.left < 0 or ballrect_big.right > width:        
        speed_big[0] = -speed_big[0]    
    if ballrect_big.top < 0 or ballrect_big.bottom > height:        
        speed_big[1] = -speed_big[1]

    screen.fill(black)            # Erase the Work space
    screen.blit(ball_big, ballrect_big)   # Combine Ball surface with workspace surface
    pygame.display.flip()         # display workspace on screen