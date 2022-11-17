import datetime

import cv2
import mss
import numpy as np
import time
import json
import os

def cv2ParseModule():
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

        lower_red = np.array([0, 50, 50])  # диапазон цвета HSV
        upper_red = np.array([10, 255, 255])
        mask0 = cv2.inRange(hsv, lower_red, upper_red)

        lower_red = np.array([170, 50, 50])
        upper_red = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        mask = mask0 + mask1

        hasRed = np.sum(mask)
        cv2.imshow("window_name", mask)
        cv2.waitKey()
        cv2.destroyAllWindows()
        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HS V)  # меняем цветовую модель с BGR на HSV
        # thresh = cv2.inRange(hsv, hsv_min, hsv_max)  # применяем цветовой фильтр
        contours0, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # перебираем все найденные контуры в цикле
        for cnt in contours0:
            rect = cv2.minAreaRect(cnt)  # пытаемся вписать прямоугольник
            print(f'пытаемся вписать прямоугольник -{bool(rect)}')
            box = cv2.boxPoints(rect)  # поиск четырех вершин прямоугольника

            box = np.int0(box)  # округление координат
            area = int(rect[1][0] * rect[1][1])  # вычисление площади
            if area > 500:
                print('TRUE')
                cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
            # cv2.drawContours(mask, [box], 0, (170, 55, 55), 2)  # рисуем прямоугольник

                cv2.imshow('contours', img)  # вывод обработанного кадра в окно

                cv2.waitKey()
                cv2.destroyAllWindows()
        # if hasRed > 10:
        #     print("ENEMY IN THE HOME")
        #     sct.shot(output=f'object_create.jpg')
        #     time.sleep(3)
        #     pass
        # else:
        #     try:
        #         os.remove(path)
        #     except (FileNotFoundError, PermissionError):
        #         pass
        #
        #     print("RED NOT detected!")
        #     time.sleep(0.3)
        #     print("New search...")
        #     last_time = time.time()

if __name__ == '__main__':
    cv2ParseModule()