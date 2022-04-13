#!/usr/bin/env python
# coding: utf-8
"""
v0.2.0
Problems:
 Isn't sensitive enough
  Now that I'm blacklisting perk ycoords, try reducing detection threshold further. (In progress)
To do:
 Continue to loop detection, but multiprocess the shooting within that, so we can loop shooting as well inside the
 multiprocess, but kill it and restart it from the detection loop each time detect_fn finishes running.
 Could also use this to add back in up/down arrow starting/stopping.
     May have to switch to using input listener for this to avoid lag or having to use time.sleep().
 Add testing mode that displays detected enemy points (and eventually boxes) instead of clicking them.
  Use new OpenGL object. Add a bool constant to determine whether script is in shooting or drawing mode. 
"""

import time
print('Importing modules...')
start_time = time.time()
import keyboard
import os
import pathlib
import pyautogui
import tkinter
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import numpy as np
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import warnings
matplotlib.use('TkAgg')
from PIL import ImageGrab
import winsound
from typing import Dict, Any, Optional, List
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Suppress TensorFlow logging (1)
import tensorflow as tf
tf.get_logger().setLevel('ERROR')           # Suppress TensorFlow logging (2)
end_time = time.time()
elapsed_time = end_time - start_time
print(' Took {} seconds'.format(elapsed_time))

# Enable GPU dynamic memory allocation
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

# Disable mouse clicks:
DEBUG_MOUSE=False
# Show detections dictionary structure:
DEBUG_DETECTIONS=False
# Show clicked enemy locations:
DEBUG_LOCATIONS=True
# Show total yblacklist detections: 
DEBUG_YBLACKLIST=False
# Show individual yblacklist detections: 
DEBUG_YBLACKLIST_2=False

# Screen capture stuff 1560x700
SCREENTOP = 100
SCREENBOT = 800
SCREENLFT = 160
SCREENRGT = 1720
IM_WIDTH = SCREENRGT-SCREENLFT
IM_HEIGHT = SCREENBOT-SCREENTOP

IMAGE_PATHS = ['img.jpg']
#PATH_TO_SAVED_MODEL = "exported-models\my_model_1\saved_model" # Old model (#1)
PATH_TO_SAVED_MODEL = "exported-models\my_model\saved_model" # New model (#2)
PATH_TO_LABELS = 'annotations\label_map.pbtxt'

# Load saved model and build the detection function
print('Loading model...')
start_time = time.time()
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
end_time = time.time()
elapsed_time = end_time - start_time
print(' Took in {} seconds'.format(elapsed_time))

# Load label map data (for plotting)
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

def autoclicker():
    print("Starting Autoclicker.")
    winsound.Beep(528, 500)
    # Define known problem ycoords to skip:
    yblacklist = [  # Name             # Detectable at
        '407', #          Luck perk      0.951
        '408', #          Luck perk      0.864
        '413', #         Swift perk      0.917
        '416', #      Regrowth perk      0.861 <---
        '430', #      Catalyst perk      0.896
        '450', #                  ?      ?
        '458', #      Friction perk      0.876 <--
        '425', #        Growth perk      0.977
        '427', #        Growth perk      0.973
        '452', #         Wound perk      0.966
        '484', #      Catalyst perk      0.993
        '510', #        Growth perk      0.859 <----
        '516', #         Focus perk      0.931
        '517', #          Rush perk      0.905
        '554', #     Precision perk      0.966
        '555', #        Growth perk      0.960
        '556', #         Wound perk      0.970
        '558', #        Growth perk      0.941
        '561', #      Catalyst perk      0.992
        '562', #         Wound perk      0.967
        '559', #         Wound perk      0.943
        '653', #         Souls perk text 0.932
        '650', #     Stability perk text 0.892 <
        '676', #         Wound perk      0.966
        '675', #         Cloak perk text 0.860 <---
        '677', #      Immortal perk text 0.851 <----
        '678', #       Barrier perk text 0.970
        '679', #       Barrier perk text 0.975
        '693', # Fragmentation perk text 0.987
        '680', #      Immortal perk text 0.967
        '682', #      Immortal perk text 0.856 <---
        '687', #   Will-O-Wisp perk text 0.919
        '707', # Fragmentation perk text 0.873 <--
        ]
    while True:
        if keyboard.is_pressed('down'):
            print("Stopping Autoclicker...")
            #if not DEBUG_MOUSE: pyautogui.mouseUp() # Disabled to debug perk menu
            winsound.Beep(432, 500)
            return

        #image_np = np.array(Image.open('img.jpg'))
        image_np = np.array(ImageGrab.grab(bbox=(SCREENLFT, SCREENTOP, SCREENRGT, SCREENBOT)))

        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(image_np)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]

        detections = detect_fn(input_tensor)

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(detections.pop('num_detections')) # What does .pop do?
        detections = {key: value[0, :num_detections].numpy()
                               for key, value in detections.items()}
        detections['num_detections'] = num_detections
        # Is always '100' for some reason:
        #print("num_detections: " + str(detections['num_detections']))

        # detection_classes should be ints. Commented since not using yet.
        #detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        if DEBUG_DETECTIONS:
            for key, value in detections.items():
                print(key, ' : ', value)

        counter = 0
        enemies = 0
        blacklisted = 0
        for target in detections['detection_scores']:

            # Shoot definite enemies. <disabled>If definite enemy detected, also shoot less confident enemies</disabled>:
            #if target > 0.90:# or (target > 0.90 and enemies > 0):
            if target > 0.85:

                # Get location of identified enemy in form of tensors representing bounding box:
                ymin = detections['detection_boxes'][counter][0]
                xmin = detections['detection_boxes'][counter][1]
                ymax = detections['detection_boxes'][counter][2]
                xmax = detections['detection_boxes'][counter][3]

                # Convert tensors to coordinates and normalize them to screencap size:
                (left, right, top, bottom) = (xmin * IM_WIDTH, xmax * IM_WIDTH, ymin * IM_HEIGHT, ymax * IM_HEIGHT)

                # Find center of bounding box:
                xcoord_float = ((right+left)/2)
                ycoord_float = ((bottom+top)/2)

                # Remove everything after decimal to get an int, compensating for screencap boundaries:
                xcoord = int(str(xcoord_float).split('.')[0])+SCREENLFT
                ycoord = int(str(ycoord_float).split('.')[0])+SCREENTOP

                # Ignore known problem locations:
                ignore = False
                for coord in yblacklist:
                    if str(ycoord) == coord: # Remove everything after decimal
                        if DEBUG_YBLACKLIST_2: print("! Ignoring blacklisted ycoord: " + str(ycoord))
                        blacklisted += 1
                        ignore = True

                # Shoot
                if not ignore:
                    enemies += 1
                    if DEBUG_LOCATIONS: print(" Score: " + str(target) + " Loc: " + str(xcoord) + ", " + str(ycoord))
                    pyautogui.moveTo(xcoord, ycoord)

            counter += 1

        # Check to change click status once per detection cycle:
        if enemies > 0:
            if not DEBUG_MOUSE: pyautogui.mouseDown()
        #else: # Removed to get more shots out
        #    if not DEBUG_MOUSE and not DEBUG_PERKS:
        #        pyautogui.mouseUp()

        if enemies > 0:
            print(" Shot " + str(enemies) + " enemies")
        if DEBUG_YBLACKLIST: 
            if blacklisted > 0:
                print("! Skipped " + str(blacklisted) + " blacklisted ycoords")

def main():
    autoclicker()

if __name__ == "__main__":
    main()
