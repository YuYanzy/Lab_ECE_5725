#! /usr/bin/python
from pygame.locals import *
import RPi.GPIO as GPIO
import pygame
import time 
import os, sys

# set up the enviroments
os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

#setting the GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#setting up PWM and GPIO pin
GPIO.setup(16, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#stopped to start
frequency = 1
left_pwm = GPIO.PWM(26, frequency)
right_pwm = GPIO.PWM(16, frequency)
left_duty_cycle = 0
right_duty_cycle = 0
left_pwm.start(0)
right_pwm.start(0)

# global flags to control the program
CODERUN = True
PANIC_STOP = False
START_GAME = False
GAME_EVENT = 0
start_time = time.time()

# global flags to control left wheel
left_motion_control_flag = False
left_direction_control_flag = True
# Log data structer for the left wheel
left_log_dict = {(10, 100): ["Stop", "0"], (10, 120): ["Stop", "0"], (10, 140): ["Stop", "0"]}
left_log_position_hash_dict = {1:(10, 100), 2: (10, 120), 3: (10, 140) }
# global flags to control right wheel
right_motion_control_flag = False
right_direction_control_flag = True
# Log data structer for the right wheel
right_log_dict = {(220, 100): ["Stop", "0"], (220, 120): ["Stop", "0"], (220, 140): ["Stop", "0"]}
right_log_position_hash_dict = {1:(220, 100), 2: (220, 120), 3: (220, 140)}

def upload_log(side, event_type, elapse_time):
    if side == 'left':
        print("Update the left_log")
        log_dict = left_log_dict
        has_dict = left_log_position_hash_dict
    else:
        print("Update the right_log")
        log_dict = right_log_dict
        has_dict = right_log_position_hash_dict
    log_dict[has_dict[3]] = log_dict[has_dict[2]]
    log_dict[has_dict[2]] = log_dict[has_dict[1]]
    log_dict[has_dict[1]] = [event_type, str(int(elapse_time))]
    print(log_dict)
    print('\n')

def left_wheel_start():
    global left_duty_cycle, left_motion_control_flag, start_time
    left_motion_control_flag = True
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(6, GPIO.LOW)
    left_duty_cycle = 50
    left_pwm.ChangeDutyCycle(left_duty_cycle)
    elapse_time = time.time() - start_time
    upload_log(side="left", event_type="Start", elapse_time=elapse_time)

def left_wheel_stop():
    global left_duty_cycle, left_motion_control_flag, left_direction_control_flag, start_time
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.LOW)
    left_duty_cycle = 0
    left_pwm.ChangeDutyCycle(left_duty_cycle)
    left_motion_control_flag = False
    left_direction_control_flag = True # set the defult direction back to clockwise
    elapse_time = time.time() - start_time
    upload_log(side="left", event_type="Stop", elapse_time=elapse_time)

def left_wheel_counterclockwise():
    global left_direction_control_flag, start_time
    left_direction_control_flag = False
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.HIGH)
    elapse_time = time.time() - start_time
    upload_log(side="left", event_type="Counter-Clk", elapse_time=elapse_time)

def left_wheel_clockwise():
    global left_direction_control_flag, start_time
    left_direction_control_flag = True
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(6, GPIO.LOW)
    elapse_time = time.time() - start_time
    upload_log(side="left", event_type="Clkwise", elapse_time=elapse_time)

def right_wheel_start():
    global right_motion_control_flag, right_duty_cycle, start_time
    right_motion_control_flag = True
    GPIO.output(19, GPIO.HIGH)
    GPIO.output(13, GPIO.LOW)
    right_duty_cycle = 50
    right_pwm.ChangeDutyCycle(right_duty_cycle)
    elapse_time = time.time() - start_time
    upload_log(side="right", event_type="Start", elapse_time=elapse_time)

def righ_wheel_stop():
    global right_motion_control_flag, right_duty_cycle, right_direction_control_flag, start_time
    right_motion_control_flag = False
    right_direction_control_flag = True # set the defult direction back to clockwise
    GPIO.output(19, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    right_duty_cycle = 0
    right_pwm.ChangeDutyCycle(right_duty_cycle)
    elapse_time = time.time() - start_time
    upload_log(side="right", event_type="Stop", elapse_time=elapse_time)

def right_wheel_counterclockwise():
    global right_direction_control_flag, start_time
    right_direction_control_flag = False
    GPIO.output(19, GPIO.LOW)
    GPIO.output(13, GPIO.HIGH)
    elapse_time = time.time() - start_time
    upload_log(side="right", event_type="Counter-Clk", elapse_time=elapse_time)

def right_wheel_clockwise():
    global right_direction_control_flag, start_time
    right_direction_control_flag = True
    GPIO.output(19, GPIO.HIGH)
    GPIO.output(13, GPIO.LOW)
    elapse_time = time.time() - start_time
    upload_log(side="right", event_type="Clkwise", elapse_time=elapse_time)

def move_forward():
    left_wheel_start()
    right_wheel_start()

def move_backword():
    left_wheel_counterclockwise()
    right_wheel_counterclockwise()

def stop():
    left_wheel_stop()
    righ_wheel_stop()

def pivot_left():
    righ_wheel_stop()

def pivot_right():
    right_wheel_start()

def GPIO27_callback(channel):
    global CODERUN
    print("Button 27 has been pressed, quit the program\n")
    CODERUN = False

# Initialize the Pygame 
pygame.init()
pygame.mouse.set_visible(False)
# Basic configuration for the game
size = (width, height) = (320, 240)
screen = pygame.display.set_mode(size)
FPS = 40
clock = pygame.time.Clock()
WHITE = 255,255,255
BLACK = 0,0,0
RED = 255,0,0
GREEN = 0,255,0
# Button and Text info configuration
history_content_font = pygame.font.Font(None, 20)
history_title_font = quit_button_font = pygame.font.Font(None, 30)
center_button_font = pygame.font.Font(None, 40)
quit_button = {"Start": (50,220), "Quit":(270, 220)}
stop_button = {'STOP': (160, 120)}

def draw_buttons():
    # draw the quit button
    for text, position in quit_button.items():
        text_surface = quit_button_font.render(text, True, WHITE)
        rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, rect)
    
    # draw the center button
    for text, position in stop_button.items():
        if PANIC_STOP:
            text = "RESMU"
        text_surface = center_button_font.render(text, True, BLACK)
        rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, rect)

def draw_circle():
    if PANIC_STOP:
        # draw green color when panic stopped
        pygame.draw.circle(screen, GREEN, (160,120), 50)
    else:
        # draw red color when not panic stopped
        pygame.draw.circle(screen, RED, (160,120), 50)

def draw_log_title(side='left'):
    if side == 'left':
        text = 'Left History'
        position = (5, 60)
    else:
        text = "Rigt History"
        position = (205, 60)
    text_surface = history_title_font.render(text, True, WHITE)
    rect = text_surface.get_rect(midleft=position)
    screen.blit(text_surface, rect)

def draw_log_content(side='left'):
    if side == 'left':
        log_dict = left_log_dict
    else:
        log_dict = right_log_dict
    # Data Example: (10, 100): ["Stop", "0"]
    for position,  content in log_dict.items():
        # draw the command
        text_surface = history_content_font.render(content[0], True, WHITE)
        rect = text_surface.get_rect(midleft=position)
        screen.blit(text_surface, rect)
        # draw the number
        text_surface = history_content_font.render(content[1], True, WHITE)
        rect = text_surface.get_rect(midleft=( position[0] + 80, position[1]))
        screen.blit(text_surface, rect)

def draw_log_history():
    # draw the left side
    draw_log_title("left")
    draw_log_content("left")
    # draw the right side
    draw_log_title("right")
    draw_log_content("right")

def draw_game():
    screen.fill(BLACK)
    draw_circle()
    draw_buttons()
    draw_log_history()
    pygame.display.flip()

def check_start_button(touch_position):
    x,y = touch_position
    # Check if the touch position is in the button area
    if (y < 240 and y > 200) and (x < 80 and x > 20):
        global START_GAME
        START_GAME = True
        print("Start The GAME!!!")

def check_quit_button(touch_position):
    x, y = touch_position
    # Check if the touch position is in the button area
    if (y < 240 and y > 200) and (x < 290 and x > 240):
        print("The quit button is pressed, quit the game!\n")
        global CODERUN
        CODERUN = False

def check_center_button(touch_position):
    x, y = touch_position
    # Check if the touch position is in the button area
    if (y < 220 and y > 100) and (x < 220 and x > 100):
        global PANIC_STOP, START_GAME
        PANIC_STOP = not PANIC_STOP
        START_GAME = not START_GAME
        if PANIC_STOP:
            print("The PANIC STOP button is pressed! PANIC STOP!!!\n")
            left_wheel_stop()
            righ_wheel_stop()
        else:
            print("The RESUME button is pressed! RESUME!!!\n")
            left_wheel_start()
            right_wheel_start()


def run_game_event(event_number):
    if event_number == 0:
        print("Move the robot forward about 1 foot\n")
        move_forward()
    elif event_number == 1:
        print("Stop\n")
        stop()
    elif event_number == 2:
        print("Move the robot backwards about 1 foot\n")
        move_backword()
    elif event_number == 3:
        print("Pivot left\n")
        pivot_left()
    elif event_number == 4:
        print("Stop\n")
        stop()
    elif event_number == 5:
        print("Pivot right\n")
        pivot_right()
    elif event_number == 6:
        print("Stop\n")
        stop()
        print("Back to the top\n")


if __name__ == "__main__":
    # add detect event
    GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=500)
    draw_game()
    try:
        while (time.time() - start_time <= 5000 and CODERUN):
            clock.tick(FPS)
            touch_position = None
            for event in pygame.event.get(): 
                if(event.type is MOUSEBUTTONDOWN): 
                    pass
                elif(event.type is MOUSEBUTTONUP):
                    touch_position = pygame.mouse.get_pos()
                    print(touch_position)
                    check_start_button(touch_position)
                    check_quit_button(touch_position)
                    check_center_button(touch_position)
            if START_GAME:
                run_game_event(event_number=GAME_EVENT)
                GAME_EVENT = (GAME_EVENT + 1) % 7
                draw_game()
                time.sleep(2)
            else:
                draw_game()


    except KeyboardInterrupt:
        try:
            print("\nKeyboardInterrupt, clean every thing and exit!")
            left_pwm.stop()
            right_pwm.stop()
            GPIO.cleanup()
            pygame.display.quit()
            pygame.quit()
            sys.exit(0)
        except SystemExit:
            # print("Somthing Wrong, clean every thing and exit!")
            left_pwm.stop()
            right_pwm.stop()
            GPIO.cleanup()
            pygame.display.quit()
            pygame.quit()
            os._exit(0)


