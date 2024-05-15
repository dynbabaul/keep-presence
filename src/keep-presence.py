#!/usr/bin/env python3

import argparse
import time
from datetime import datetime
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import random
from threading import Thread
from time import sleep

mouse = MouseController()
keyboard = KeyboardController()

MOVE_MOUSE = False
SCROLL_ACTION = False
PRESS_SHIFT_KEY = False
RANDOM_MODE = False
PIXELS_TO_MOVE = 1
RAND_INTERVAL_START = 0
RAND_INTERVAL_STOP = 0
TIMEOUT = 0
TIMEOUT_MESSAGE = ""

move_mouse_every_seconds = 300
mouse_direction = 0
currentPosition = []
lastSavePosition = (0, 0)

def define_custom_seconds():
    global move_mouse_every_seconds, PIXELS_TO_MOVE, PRESS_SHIFT_KEY, MOVE_MOUSE, SCROLL_ACTION, \
        RANDOM_MODE, RAND_INTERVAL_START, RAND_INTERVAL_STOP, TIMEOUT, TIMEOUT_MESSAGE

    parser = argparse.ArgumentParser(
        description="This program moves the mouse or press a key when it detects that you are away. "
                    "It won't do anything if you are using your computer. "
                    "Useful to trick your machine to think you are still working with it.")

    parser.add_argument(
        "-s", "--seconds", type=int,
        help="Define in seconds how long to wait after a user is considered idle. Default 300.")

    parser.add_argument(
        "-p", "--pixels", type=int,
        help="Set how many pixels the mouse should move. Default 1.")

    parser.add_argument(
        "-m", "--mode",
        help="Available options: keyboard, mouse, both (mouse & keyboard) and scroll; default is mouse. "
             "This is the action that will be executed when the user is idle: "
             "If keyboard is selected, the program will press the shift key. "
             "If mouse is selected, the program will move the mouse. "
             "If both is selected, the program will do both actions. ")

    parser.add_argument(
        "-r", "--random", type=int, nargs=2,
        help="Usage: two numbers (ex. -r 3 10). "
             "Execute actions based on a random interval between start and stop seconds. "
             "Note: Overwrites the seconds argument.")

    parser.add_argument(
        "-t", "--timeout",
        help="Define a time limit to run in  (s)econds, (m)inutes or (h)ours. "
             "Example: 10s for 10 seconds, 10m for 10 minutes, 10h for 10 hours. "
             "Program will close after this amount of time. ")

    args = parser.parse_args()
    mode = args.mode
    random_seconds_interval = args.random
    tout = args.timeout

    if tout:
        if tout.lower().endswith("s"):
            TIMEOUT_MESSAGE = tout[:-1] + " seconds"
            TIMEOUT = int(tout[:-1])
        elif tout.lower().endswith("m"):
            TIMEOUT_MESSAGE = tout[:-1] + " minutes"
            TIMEOUT = int(tout[:-1]) * 60
        elif tout.lower().endswith("h"):
            TIMEOUT_MESSAGE = tout[:-1] + " hours"
            TIMEOUT = int(tout[:-1]) * 60 * 60
        else:
            print("Error: Invlaid time specified. Please use (s)econds, (m)inutes or (h)ours in your timeout.")
            exit()

    if args.seconds:
        move_mouse_every_seconds = int(args.seconds)

    if args.pixels:
        PIXELS_TO_MOVE = int(args.pixels)

    if random_seconds_interval:
        RAND_INTERVAL_START = int(random_seconds_interval[0])
        RAND_INTERVAL_STOP = int(random_seconds_interval[1])

        # prevents initialize random.randint() with invalid numbers:
        if RAND_INTERVAL_START > RAND_INTERVAL_STOP:
            print("Error: Random initial number needs to be lower than random limit number.")
            exit()

    is_both_enabled = 'both' == mode
    is_keyboard_enabled = 'keyboard' == mode or is_both_enabled
    is_mouse_enabled = 'mouse' == mode or is_both_enabled or mode is None
    is_scroll_enabled = 'scroll' == mode

    print('--------')
    if is_keyboard_enabled:
        PRESS_SHIFT_KEY = True
        print(get_now_timestamp(), "Keyboard is enabled")

    if is_scroll_enabled:
        SCROLL_ACTION = True
        print(get_now_timestamp(), "Mouse wheel scroll is enabled")

    if is_mouse_enabled:
        MOVE_MOUSE = True
        print(get_now_timestamp(), "Mouse is enabled, moving", PIXELS_TO_MOVE, 'pixels')

    if random_seconds_interval:
        RANDOM_MODE = True
        print(get_now_timestamp(), "Random timing is enabled.")
    else:
        print(get_now_timestamp(), 'Running every', str(move_mouse_every_seconds), 'seconds')

    if TIMEOUT:
        print(get_now_timestamp(), "Timeout is set for " + TIMEOUT_MESSAGE + ".")

    print('--------')


def move_mouse_when_unable_to_move(expected_mouse_position):
    if expected_mouse_position != mouse.position:
        mouse.position = (PIXELS_TO_MOVE, PIXELS_TO_MOVE)


def move_mouse():
    global mouse_direction, currentPosition
    delta_x = PIXELS_TO_MOVE if mouse_direction == 0 or mouse_direction == 3 else -PIXELS_TO_MOVE
    delta_y = PIXELS_TO_MOVE if mouse_direction == 0 or mouse_direction == 1 else -PIXELS_TO_MOVE

    new_x = currentPosition[0] + delta_x
    new_y = currentPosition[1] + delta_y
    #mouse_direction = (mouse_direction) % 4

    old_position = mouse.position
    new_position = (new_x, new_y)
    mouse.position = new_position

    move_mouse_when_unable_to_move(new_position)

    current_position = mouse.position

    print(get_now_timestamp(), 'Moved mouse to: ', current_position)

    time.sleep(0.2)
    mouse.position = old_position

    move_mouse_when_unable_to_move(old_position)

    current_position = mouse.position

    print(get_now_timestamp(), 'Moved mouse to: ', current_position)

    return current_position


def mouse_wheel_scroll():
    mouse.scroll(0, -2)
    print(get_now_timestamp(), 'Mouse wheel scrolled')


def press_shift_key():
    keyboard.press(Key.shift)
    keyboard.release(Key.shift)
    print(get_now_timestamp(), 'Shift key pressed')


def get_now_timestamp():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def execute_keep_awake_action():
    print(get_now_timestamp(), 'Idle detection')

    if MOVE_MOUSE:
        move_mouse()

    if SCROLL_ACTION:
        mouse_wheel_scroll()

    if PRESS_SHIFT_KEY:
        press_shift_key()


define_custom_seconds()


def mainfunc():
    global lastSavePosition, currentPosition

    try:
        while 1:
            currentPosition = mouse.position
            is_user_away = currentPosition == lastSavePosition

            if is_user_away:
                execute_keep_awake_action()
                currentPosition = mouse.position

            if not is_user_away:
                print(get_now_timestamp(), 'User activity detected')

            lastSavePosition = currentPosition

            if RANDOM_MODE:
                rand_delay = random.randint(RAND_INTERVAL_START, RAND_INTERVAL_STOP)
                print(get_now_timestamp(), f"Delay: {str(rand_delay)}")
                time.sleep(rand_delay)
            else:
                time.sleep(move_mouse_every_seconds)

            print('--------')

    except KeyboardInterrupt:
        print("\nBye bye ;-)")
        exit()



t = Thread(target=mainfunc, daemon=True)
t.start()

try:
    if TIMEOUT:
        sleep(TIMEOUT)
        print(get_now_timestamp(), "Timeout for " + TIMEOUT_MESSAGE + " has elapsed, program is closing.")
    else:
        while True:
            pass

except KeyboardInterrupt:
    print("\nBye bye ;-)")
    exit()
