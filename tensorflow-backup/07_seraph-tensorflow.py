#!/usr/bin/env python
# coding: utf-8
"""
v0.1.2
Problems:
 Isn't sensitive enough
  Solution: Try reducing initial detection threshold (Complete. Continue evaluating before further tuning)
To do:
 Refine blacklist into ranges instead of specific values. Or just match up to before decimal? try splitting string at '.'
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
#gpus = tf.config.experimental.list_physical_devices('GPU')
#for gpu in gpus:
#    tf.config.experimental.set_memory_growth(gpu, True)

# Disables mouse clicks if true
DEBUG_MOUSE=False
# Show detections dictionary structure:
DEBUG_DETECTIONS=False

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
    yblacklist = [            # Name                   # Detectable at
        '450.0',              # Annoying invisible enemy. idk what this is
        '484.4199299812317',  #   Damage upgrade perk. 0.992
        '484.48014706373215', #   Damage upgrade perk. 0.992
        '484.3454122543335',  #   Damage upgrade perk. 0.993
        '425.92676877975464', #           Growth perk. 0.977
        '425.7742702960968',  #           Growth perk. 0.977
        '554.9560904502869',  #           Growth perk. 0.977
        '678.6397874355316',  #     Barrier perk text. 0.975
        '679.2737305164337',  #     Barrier perk text. 0.975
        '427.28709280490875', #           Growth perk. 0.973
        '678.9040207862854',  # Thunderbolt perk text. 0.972
        '678.1638085842133'   #     Barrier perk text. 0.970
        '680.664324760437',   #    Immortal perk text. 0.967
        '680.8577537536621',  #    Immortal perk text. 0.967
        '562.5507235527039',  #            Wound perk. 0.967
        '562.6172304153442',  #   Damage upgrade perk. 0.966
        '680.8537483215332',  #    Immortal perk text. 0.966
        '676.8829464912415',  #            Wound perk. 0.966
        '554.4820725917816',  #        Precision perk. 0.966
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

        #print("Detecting...")
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
        #print("Shooting...")
        for target in detections['detection_scores']:
            #counter += 1 # Moved to end of loop
            # Shoot definite enemies. If definite enemy detected, also shoot less confident enemies:
            if target > 0.96:# or (target > 0.90 and enemies > 0):
                # Get location of identified enemy in form of tensors representing bounding box:
                ymin = detections['detection_boxes'][counter][0]
                xmin = detections['detection_boxes'][counter][1]
                ymax = detections['detection_boxes'][counter][2]
                xmax = detections['detection_boxes'][counter][3]

                # Convert tensors to coordinates and normalize them to screencap size:
                (left, right, top, bottom) = (xmin * IM_WIDTH, xmax * IM_WIDTH, ymin * IM_HEIGHT, ymax * IM_HEIGHT)

                # Find center of bounding box and compensate for screencap boundaries:
                xcoord = ((right+left)/2)+SCREENLFT
                ycoord = ((bottom+top)/2)+SCREENTOP

                # Ignore known problem locations:
                ignore = False
                for coord in yblacklist:
                    if str(ycoord) == coord:
                        print("! Ignoring blacklisted ycoord: " + str(ycoord))
                        ignore = True

                if not ignore:
                    enemies += 1
                    print(" Score: " + str(target) + " Loc: " + str(xcoord) + ", " + str(ycoord))
                    pyautogui.moveTo(xcoord, ycoord)

            # Check to change click status once per detection cycle:
            counter += 1
            if counter == 1:
                if enemies > 0:
                    if not DEBUG_MOUSE: pyautogui.mouseDown()
                else:
                    if not DEBUG_MOUSE: pyautogui.mouseUp()

        if enemies > 0:
            print(" Shot " + str(enemies) + " enemies.")

def main():
    autoclicker()

if __name__ == "__main__":
    main()
