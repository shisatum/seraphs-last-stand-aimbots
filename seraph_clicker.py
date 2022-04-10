"""
Seraph's Last Stand auto-clicker v0.1
Prereqs: Win10, Python3, 1920x1080p
"""
import keyboard
import pyautogui
import time
import winsound

def main():
    autoclicker_running = False
    print("Switch to game, then hold uparrow to start and downarrow to stop.")
    print("Hold Shift to re-engage after perk menu. Ctrl+c to quit.")
    while True: 
        time.sleep(0.5) # Sleep to avoid input lag in-game. 
        if autoclicker_running and keyboard.is_pressed('shift'):
            pyautogui.mouseDown()
        try:
            if keyboard.is_pressed('up'):
                if not autoclicker_running:
                    winsound.Beep(512, 500)
                    autoclicker_running = True
                    pyautogui.mouseDown()
                    print("Started autoclicker")
            elif keyboard.is_pressed('down'):
                if autoclicker_running:
                    winsound.Beep(432, 500)
                    autoclicker_running = False
                    pyautogui.mouseUp()
                    print("Stopped autoclicker")
        except:
            break

if __name__ == "__main__":
    main()
