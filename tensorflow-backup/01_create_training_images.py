"""
Seraph's Last Stand OpenCV aimbot v0.2.0
Prereqs: Win10, Python3, 1920x1080p
"""
import cv2
import keyboard
import math
import multiprocessing
import numpy as np
from PIL import ImageGrab
import pyautogui
import time
import winsound

# Screen capture stuff
SCREENTOP = 100
SCREENBOT = 800
SCREENLFT = 160
SCREENRGT = 1720

def capture_screen():
    """ Capture screen """
    frame_bgr = np.array(ImageGrab.grab(bbox=(SCREENLFT, SCREENTOP, SCREENRGT, SCREENBOT)))
    return frame_bgr

def autoclicker():
    """ Take x screenshots, one every x seconds """
    #num_captures = 100 # Training/test data (for actual training)
    num_captures = 20
    while num_captures > 0:
        num_captures -= 1
        time.sleep(10) # Delay
        frame_bgr = capture_screen()
        cv2.imwrite('images/'+str(num_captures)+'cap.jpg', frame_bgr)

    winsound.Beep(432, 500)

def main():
    autoclicker_running = False
    print("Switch to game, then hold uparrow to start and downarrow to stop.")
    print("Ctrl+c to quit.")
    while True:
        time.sleep(0.5)
        try:
            if keyboard.is_pressed('up'):
                if not autoclicker_running:
                    winsound.Beep(528, 500)
                    autoclicker_running = True
                    p = multiprocessing.Process(target=autoclicker, name="Autoclicker")
                    p.start()
                    print("Started aimbot")
            elif keyboard.is_pressed('down'):
                if autoclicker_running:
                    winsound.Beep(432, 500)
                    autoclicker_running = False
                    p.terminate()
                    p.join()
                    print("Stopped aimbot")
        except:
            break

if __name__ == "__main__":
    main()
