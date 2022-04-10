"""
Seraph's Last Stand aimbot v0.3
Prereqs: Win10, Python3, 1920x1080p
"""
import keyboard
import multiprocessing
import pyautogui
import time
import winsound

DEBUG=False
color = (255, 255, 255)           # Enemy
left_start=300                    # Define region of screen to check
top_start=113                     # 
right_end=1920-(left_start*2)     # 
bottom_end=(1080-(top_start*2))/2 # Was 435
aim_offset=30                     # Lazy attempt to center aim on target

def autoclicker():
    while True:
        if keyboard.is_pressed('shift'):
            time.sleep(0.5)
        else:
            has_target = False
            s = pyautogui.screenshot(region=(left_start, top_start, right_end, bottom_end))
            if DEBUG: print("Took screenshot")
            for x in range(s.width):
                for y in range(s.height):
                    if s.getpixel((x, y)) == color:
                        pyautogui.mouseDown()
                        pyautogui.moveTo(x+left_start+aim_offset, y+top_start)
                        if DEBUG: print("Moved cursor to " + str(x+left_start+aim_offset) + "," + str(y+top_start))
                        has_target = True
                        break
                if has_target:
                    break

def main():
    autoclicker_running = False
    if DEBUG: print("Debug mode active.")
    print("Switch to game, then hold uparrow to start and downarrow to stop.")
    print("Hold Shift to allow manual aim. Ctrl+c to quit.")
    while True: 
        time.sleep(0.5) # Sleep to avoid input lag in-game. The rest of the lag comes from the screenshot in autoclicker() being too big.
        try:            # Need to try opencv
            if keyboard.is_pressed('up'):
                if not autoclicker_running:
                    winsound.Beep(512, 500)
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
                    pyautogui.mouseUp()
                    print("Stopped aimbot")
        except:
            break

if __name__ == "__main__":
    main()
