import datetime

import cv2
import mss
import numpy as np
import time
import json
import os


sct = mss.mss()
last_time = time.time()

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'object_create.jpg')

with open('mouse_poss\mouse_poss.json') as file:
    parse_area = json.load(file)

while True:
    if time.time() - last_time < 2:
        continue

    img = np.asarray(sct.grab(parse_area))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([281, 90, 46])  # диапазон цвета HSV
    upper_red = np.array([328, 90, 46])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    mask = mask0 + mask1

    hasRed = np.sum(mask)
    if hasRed > 0:
        print("ENEMY IN THE HOME")
        time.sleep(1)
        sct.shot(output=f'object_create.jpg')
        pass
    else:

        try:
            os.remove(path)
        except FileNotFoundError as EX:
            print(EX)

        print("RED NOT detected!")
        time.sleep(0.3)
        print("New search...")
        last_time = time.time()