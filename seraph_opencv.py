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

DEBUG_RUNNING=False
DEBUG_PERKS=False
DEBUG_CLICKED=False
DEBUG_SHOOTING=False
DEBUG_LOCATIONS=False

# Screen capture stuff
SCREENTOP = 100
SCREENBOT = 800
SCREENLFT = 160
SCREENRGT = 1720

TEMPLATE = cv2.imread('enemy_segment.png', 0)
TEMPLATE_W, TEMPLATE_H = TEMPLATE.shape[::-1]
PERK_TEMPLATE = cv2.imread('perk_menu.png', 0)

def capture_screen():
    """ Captures screen """
    frame_bgr = np.array(ImageGrab.grab(bbox=(SCREENLFT, SCREENTOP, SCREENRGT, SCREENBOT)))
    return frame_bgr

def convert_gray(frame_bgr):
    """ Converts captured screen to gray """
    frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    return frame_gray

def find_birds(frame_gray):
    """ Template matches and returns matched birds """
    bird_candidates = cv2.matchTemplate(image=frame_gray, templ=TEMPLATE, method=cv2.TM_CCOEFF_NORMED)
    definite_birds = np.where(bird_candidates >= 0.7) # Filter results with 70% confidence
    return definite_birds

def find_perks(frame_gray):
    """ Template matches and returns matched perks """
    perk_candidates = cv2.matchTemplate(image=frame_gray, templ=PERK_TEMPLATE, method=cv2.TM_CCOEFF_NORMED)
    definite_perks = np.where(perk_candidates >= 0.9) # Filter results with 90% confidence
    return definite_perks

def shoot_birds(definite_birds):
    """ Moves mouse to the matched locations """
    if DEBUG_SHOOTING: print("      Shooting")
    just_shot_coords = []
    for bird in zip(*definite_birds[::-1]):
        abs_x = int(bird[0] + TEMPLATE_W / 2) + SCREENLFT
        abs_y = int(bird[1] + TEMPLATE_H / 2) + SCREENTOP

        # Check if the target is close to somewhere we just shot
        too_close = False
        for jsa in just_shot_coords:
            dist = math.dist(jsa, [abs_x, abs_y])
            if (dist < min([TEMPLATE_W, TEMPLATE_H])):
                too_close = True
                break
        if (too_close):
            continue

        # Move mouse to target
        if DEBUG_LOCATIONS: print("        Shot at " + str(abs_x) + "," + str(abs_y))
        pyautogui.moveTo(abs_x, abs_y)
        just_shot_coords.append((abs_x, abs_y))

def autoclicker():
    clicked = False # Change to at_perk_menu?
    if DEBUG_RUNNING: print("  Started process")
    while True:
        if DEBUG_RUNNING: print("    Started iteration")
        if DEBUG_CLICKED: print("      Clicked: " + str(clicked))
        frame_bgr = capture_screen()
        frame_gray = convert_gray(frame_bgr)
        definite_perks = find_perks(frame_gray)
        definite_birds = find_birds(frame_gray)

        # Pause if at perk selection screen
        num_perks = set()
        for perk in zip(*definite_perks[::-1]):
            num_perks.add(perk)
        if DEBUG_PERKS: print("      Perks: " + str(len(num_perks)))
        if len(num_perks) > 2:
            if clicked:
                clicked = False
                pyautogui.mouseUp()
        else:
            if not clicked:
                clicked = True
                pyautogui.mouseDown()

        if clicked: shoot_birds(definite_birds)

def main():
    autoclicker_running = False
    print("Switch to game, then hold uparrow to start and downarrow to stop.")
    print("Ctrl+c to quit.")
    while True:
        time.sleep(0.5)
        #if DEBUG_RUNNING: print("autoclicker_running: " + str(autoclicker_running))
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
                    pyautogui.mouseUp()
                    p.terminate()
                    p.join()
                    print("Stopped aimbot")
        except:
            break

if __name__ == "__main__":
    main()
