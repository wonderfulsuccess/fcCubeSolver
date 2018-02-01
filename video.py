#!/usr/bin/python
# -*- coding: UTF-8 -*-
from sys import exit as Die
try:
    import sys
    import cv2
    from colordetection import ColorDetector
except ImportError as err:
    Die(err)


class Webcam:

    def __init__(self):
        self.cam              = cv2.VideoCapture(0)
        self.stickers         = self.get_sticker_coordinates('main')
        self.current_stickers = self.get_sticker_coordinates('current')
        self.preview_stickers = self.get_sticker_coordinates('preview')

    def get_sticker_coordinates(self, name):
        """
        Every array has 2 values: x and y.
        Grouped per 3 since on the cam will be
        3 rows of 3 stickers.

        :param name: the requested color type
        :returns: list
        """
        stickers = {
            'main': [#魔方取色块的位置
                [200, 120], [300, 120], [400, 120],
                [200, 220], [300, 220], [400, 220],
                [200, 320], [300, 320], [400, 320]
            ],
            'current': [ #当前实时取色板
                [20, 20], [54, 20], [88, 20],
                [20, 54], [54, 54], [88, 54],
                [20, 88], [54, 88], [88, 88]
            ],#上一贞取色板
            'preview': [
                [20, 130], [54, 130], [88, 130],
                [20, 164], [54, 164], [88, 164],
                [20, 198], [54, 198], [88, 198]
            ]
        }
        return stickers[name]


    def draw_main_stickers(self, frame):
        """Draws the 9 stickers in the frame."""
        for x,y in self.stickers:
            cv2.rectangle(frame, (x,y), (x+30, y+5), (255,255,255), 1)

    def draw_current_stickers(self, frame, state):
        """Draws the 9 current stickers in the frame."""
        for index,(x,y) in enumerate(self.current_stickers):
            cv2.rectangle(frame, (x,y), (x+32, y+32), ColorDetector.name_to_rgb(state[index]), -1)

    def draw_preview_stickers(self, frame, state):
        """Draws the 9 preview stickers in the frame."""
        for index,(x,y) in enumerate(self.preview_stickers):
            cv2.rectangle(frame, (x,y), (x+32, y+32), ColorDetector.name_to_rgb(state[index]), -1)

    def color_to_notation(self, color):
        """
        Return the notation from a specific color.
        We want a user to have green in front, white on top,
        which is the usual.

        :param color: the requested color
        """
        # notation = {
        #     'green'  : 'F',
        #     'white'  : 'U',
        #     'blue'   : 'B',
        #     'red'    : 'R',
        #     'orange' : 'L',
        #     'yellow' : 'D'
        # }
        notation = {
            'G': 'G',
            'W': 'W',
            'B': 'B',
            'R': 'R',
            'O': 'O',
            'Y': 'Y'
        }
        return notation[color]

    def scan(self):
        """
        Open up the webcam and scans the 9 regions in the center
        and show a preview in the left upper corner.

        After hitting the space bar to confirm, the block below the
        current stickers shows the current state that you have.
        This is show every user can see what the computer toke as input.

        :returns: dictionary
        """
        color_dic = {
            'G': 'G',
            'W': 'W',
            'B': 'B',
            'R': 'R',
            'O': 'O',
            'Y': 'Y'
        }
        sides   = {}
        preview = ['W','W','W',
                   'W','W','W',
                   'W','W','W']
        state   = [0,0,0,
                   0,0,0,
                   0,0,0]
        cube_state = ["","","","","",""]
        face_counter = 0
        face_counter_list = [
            'R',
            'B',
            'O',
            'G',
            'Y',
            'W'
        ]
        while True:
            _, frame = self.cam.read()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            key = cv2.waitKey(10) & 0xff

            # init certain stickers.
            self.draw_main_stickers(frame)
            self.draw_preview_stickers(frame, preview) 

            for index,(x,y) in enumerate(self.stickers):
                roi          = rgb[y:y+5, x:x+30]
                avg_rgb      = ColorDetector.average_rgb(roi)
                color_name   = ColorDetector.get_color_name(avg_rgb) #'B'
                state[index] = color_name

                # update when space bar is pressed.
                if key == 32:
                    preview = list(state)
                    self.draw_preview_stickers(frame, state)
                    face = self.color_to_notation(state[4])
                    print(state)
                    notation = [self.color_to_notation(color) for color in state]
                    sides[face] = notation
                    print(sides)
                #red
                elif key == 114:
                    preview = list(state)
                    state[4] = 'R'
                    self.draw_preview_stickers(frame, state)
                    face = 'R'
                    notation = [self.color_to_notation(color) for color in state]
                    notation[4] = 'R'
                    sides[face] = notation
                    print(sides)
                #green
                elif key == 103:
                    preview = list(state)
                    state[4] = 'G'
                    self.draw_preview_stickers(frame, state)
                    face = 'G'
                    notation = [self.color_to_notation(color) for color in state]
                    notation[4] = 'G'
                    sides[face] = notation
                    print(sides)
                #blue
                elif key == 98:
                    preview = list(state)
                    state[4] = 'B'
                    self.draw_preview_stickers(frame, state)
                    face = 'B'
                    notation = [self.color_to_notation(color) for color in state]
                    notation[4] = 'B'
                    sides[face] = notation
                    print(sides)
                #white
                elif key == 119:
                    preview = list(state)
                    state[4] = 'W'
                    self.draw_preview_stickers(frame, state)
                    face = 'W'
                    notation = [self.color_to_notation(color) for color in state]
                    notation[4] = 'W'
                    sides[face] = notation
                    print(sides)
                #orange
                elif key == 111:
                    preview = list(state)
                    state[4] = 'O'
                    self.draw_preview_stickers(frame, state)
                    face = 'O'
                    notation = [self.color_to_notation(color) for color in state]
                    notation[4] = 'O'
                    sides[face] = notation
                    print(sides)
                #yellow
                elif key == 121:
                    preview = list(state)
                    state[4] = 'Y'
                    self.draw_preview_stickers(frame, state)
                    face = 'Y'
                    notation = [self.color_to_notation(color) for color in state]
                    notation[4] = 'Y'
                    sides[face] = notation
                    print(sides)
            # show the new stickers
            self.draw_current_stickers(frame, state)
            # append amount of scanned sides
            text = 'scanned sides: {}/6'.format(len(sides))
            cv2.putText(frame, text, (20, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

            # quit on escape.
            if key == 27:
                break
            # show result                   
            cv2.imshow("freecreation", frame)
            

        self.cam.release()
        cv2.destroyAllWindows()
        # return sides if len(sides) == 6 else False
        return sides

webcam = Webcam()
