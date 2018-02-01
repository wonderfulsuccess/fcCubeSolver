#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename      : colordetection.py
# Author        : Kim K
# Created       : Tue, 26 Jan 2016
# Last Modified : Sun, 31 Jan 2016


# from recognize import Cubereg

from sys import exit as Die
try:
    import sys
    import numpy as np
    import pickle
except ImportError as err:
    Die(err)

# cubereg = Cubereg()
# cubereg.test_score()

class ColorDetection:

    def __init__(self):
        with open('color_detect.pickle', 'rb') as handle:
            self.clf = pickle.load(handle)

    def get_color_name(self, rgb):
        """ Get the name of the color based on the hue.

        :returns: string
        """
        data = list(rgb)
        # color = cubereg.predict([data])
        color = self.clf.predict(np.array([data]))
        return str(color[0])

    def name_to_rgb(self, name):
        """
        Get the main RGB color for a name.

        :param name: the color name that is requested
        :returns: tuple
        """
        color = {
            'R'    : (0,0,255),
            'O' : (0,165,255),
            'B'   : (255,0,0),
            'G'  : (0,255,0),
            'W'  : (255,255,255),
            'Y' : (0,255,255)
        }
        return color[name]

    def average_rgb(self, roi):
        """ Average the HSV colors in a region of interest.

        :param roi: the image array
        :returns: tuple
        """
        h   = 0
        s   = 0
        v   = 0
        num = 0
        for y in range(len(roi)):
            if y % 10 == 0:
                for x in range(len(roi[y])):
                    if x % 10 == 0:
                        chunk = roi[y][x]
                        num += 1
                        h += chunk[0]
                        s += chunk[1]
                        v += chunk[2]
        h /= num
        s /= num
        v /= num
        return (int(h), int(s), int(v))

ColorDetector = ColorDetection()
