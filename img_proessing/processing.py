import cv2
import numpy as np
from math import dist
import os
import colorsys
import pandas as pd
import tqdm
import warnings
warnings.filterwarnings("ignore")


MAIN_COLORS_HSL = {
    'red': ((330, 360), (0, 20)), 'orange': (21, 45),
    'yellow': (45, 50), 'green': (50, 165),
    'blue': (165, 230),
    'violet': (230, 325)
    }


def find_neighbour_color(color):
    color_hsl, bl, wh = colorsys.rgb_to_hsv(*color)
    color_hsl *= 360
    if abs(color[0] - color[1]) <= 10 and abs(color[2] - color[1]) <= 10 and abs(color[0] - color[2]):
        if color[0] <= 40 and color[1] <= 40 and color[2] <= 40:
            return 'black'
        if color[0] >= 240 and color[1] >= 240:
            return 'white'
        return 'gray'
    # color_hsl = colorsys.rgb_to_hls(*color)[0] * 360

    for i, j in MAIN_COLORS_HSL.items():
        if i == 'red':
            if j[0][0] <= color_hsl <= j[0][1] or j[1][0] <= color_hsl <= j[1][1]:
                return 'red'
        elif j[0] <= color_hsl <= j[1]:
            return i


def find_color(i):
    image = cv2.imread(i)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = image_rgb.reshape((-1, 3))
    Z = np.float32(pixels)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 12.0)
    center = cv2.kmeans(Z, 3, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    a = list(map(int, center[1]))
    # lst = [(a.count(i), center[2][i]) for i in range(3)]
    lst = [(a.count(0), center[2][0]), (a.count(1), center[2][1]), (a.count(2), center[2][1])]
    lst.sort(key=lambda x: -x[0])
    for i in lst:
        if i[1][0] >= 250 and i[1][1] >= 250 and i[1][2] >= 250:
            continue
        a = colorsys.rgb_to_hsv(int(i[1][0]), int(i[1][1]), int(i[1][2]))
        return a[0] * 360, a[1], a[2]




a = list(os.walk('img'))[0][2]
# f = open('data_main_color.csv', 'w')

f = open('data.csv', 'w')
f.write('img_path;color_hsv;bl;wh\n')
s = ''
for i in tqdm.tqdm(a):
    try:
        c = find_color('img/' + i)
        s+= 'img/'+i+';' + str(c[0])+';' + str(c[1])+';' + str(c[2])+'\n'
        # print('img/' + i, *c, sep=';', file=f)
        # f.write('img/' + i+';'+c+'\n')
    except:
        pass
f.write(s)
