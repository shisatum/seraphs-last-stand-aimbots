"""
Seraph's Last Stand OpenCV aimbot v0.1.3
Prereqs: Win10, Python3, 1920x1080p
"""
# To do:
# 0) Change framerate on line 44
# 1) Add pre-check for upgrade screen shape
#    In order to do this, need to functionalize each run of shoot function from main() instead of it looping infinitely within itself.
#    This also makes it easier to control the entire program.
# 2) Train a CNN to detect enemies and connect it to this script.
import cv2
import ctypes
from ctypes import c_bool
import keyboard
import math
import multiprocessing
import numpy as np
from PIL import ImageGrab
import pyautogui
import time
import winsound

#DEBUG=True
DEBUG=False

def find_and_shoot_birds():
    """ Captures screen, template matches enemy, and clicks the matched location """
    screenTOP = 100
    screenBOT = 800
    screenLFT = 160
    screenRGT = 1720

    #template = cv2.imread('enemy.png', 0)
    #template = cv2.imread('enemy_eye.png', 0)
    template = cv2.imread('enemy_segment.png', 0)
    template_w, template_h = template.shape[::-1]
    #### new ####
    #upgrade_screen_template = cv2.imread('upgrade_screen.png', 0)
    #upgrade_screen_template_w, upgrade_screen_template_h = upgrade_screen_template.shape[::-1]
    #### new ####

    framecount = 0
    while (True):

        framecount += 1
        if ((framecount % 5) != 0): # Detect every x frames?
            continue

        # Read screen
        frame_bgr = np.array(ImageGrab.grab(bbox=(screenLFT, screenTOP, screenRGT, screenBOT)))

        # Convert to gray
        frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

        # Apply template Matching
        bird_candidates = cv2.matchTemplate(image=frame_gray, templ=template, method=cv2.TM_CCOEFF_NORMED)
        definite_birds = np.where(bird_candidates >= 0.7)
        #### new ####
        #upgrade_candidates = cv2.matchTemplate(image=frame_gray, templ=upgrade_screen_template, method=cv2.TM_CCOEFF_NORMED)
        #definite_upgrades = np.where(upgrade_candidates >= 0.7)
        #dobreak = False
        #if len(definite_upgrades) > 2:
        #    print("Upgrade screen detected")
        #    winsound.Beep(532, 500)
        #    time.sleep(1)
        #    dobreak = True
        #if dobreak: break
        #### new ####

        for bird in zip(*definite_birds[::-1]):
            cv2.circle(img=frame_bgr, center=(int(bird[0] + template_w/2), int(bird[1] + template_h / 2)), radius=int(template_h/2), color=(255, 0, 0), thickness=2)
            cv2.drawMarker(img=frame_bgr, position=(int(bird[0] + template_w/2), int(bird[1] + template_h / 2)),color=(255, 0, 0), markerType=cv2.MARKER_CROSS, markerSize=30, thickness=2, line_type=cv2.LINE_4)

        just_shot_coords = []
        for bird in zip(*definite_birds[::-1]):
            abs_x = int(bird[0] + template_w / 2) + screenLFT
            abs_y = int(bird[1] + template_h / 2) + screenTOP

            # Check if the target is close to somewhere we just shot
            too_close = False
            for jsa in just_shot_coords:
                dist = math.dist(jsa, [abs_x, abs_y])
                if (dist < min([template_w, template_h])):
                    too_close = True
                    break
            if (too_close):
                continue

            # Shoot!
            if DEBUG: print("Shooting " + str(abs_x) + "," + str(abs_y))
            ctypes.windll.user32.SetCursorPos(abs_x, abs_y)
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up
            just_shot_coords.append((abs_x, abs_y))

        if DEBUG:
            pyautogui.press('esc') # Pause game
            cv2.imwrite('targets.png', frame_bgr)
            print("Saved image")
            #print("Displaying image")
            #cv2.imshow('OpenCV', cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
            #time.sleep(5)
            winsound.Beep(432, 200)
            break

def main():
    autoclicker_running = False
    if DEBUG: print("Debug mode active.")
    print("Switch to game, then hold uparrow to start and downarrow to stop.")
    print("Ctrl+c to quit.")
    while True: 
        time.sleep(0.5) # Sleep to avoid input lag in-game.
        #if DEBUG: print(autoclicker_running)
        try:
            if keyboard.is_pressed('up'):
                if not autoclicker_running:
                    winsound.Beep(528, 500)
                    autoclicker_running = True
                    p = multiprocessing.Process(target=find_and_shoot_birds, name="Autoclicker")
                    p.start()
                    print("Started aimbot")
                    if DEBUG:
                        time.sleep(1)
                        winsound.Beep(432, 500)
                        autoclicker_running = False
                        p.terminate()
                        p.join()
                        print("Stopped aimbot")
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
