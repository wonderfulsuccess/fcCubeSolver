# -*- coding: UTF-8 -*
from sys import exit as Die
try:
    import sys
    import cv2
    from colordetection import ColorDetector
    import codecs
except ImportError as err:
    Die(err)


class Webcam:

    def __init__(self):
        self.human_color=[
            'R','Y','B',
            '','','W',
            'O','G',''
        ]
        self.cam              = cv2.VideoCapture(0)
        self.stickers         =  [#魔方取色块的位置
            [200, 120], [300, 120], [400, 120],
            [200, 220], [300, 220], [400, 220],
            [200, 320], [300, 320], [400, 320]]

        self.current_stickers =[ #当前实时取色板
            [20, 20], [54, 20], [88, 20],
            [20, 54], [54, 54], [88, 54],
            [20, 88], [54, 88], [88, 88]
            ]

        self.train_data=codecs.open('data_train.csv','w',encoding='utf-8')
        self.train_data.seek(0)
        self.counter=0
        self.total=2100

    def draw_main_stickers(self, frame):
        """Draws the 9 stickers in the frame."""
        for x,y in self.stickers:
            cv2.rectangle(frame, (x,y), (x+30, y+5), (255,255,255), 1)

    def draw_current_stickers(self, frame, state):
        """Draws the 9 current stickers in the frame."""
        for index,(x,y) in enumerate(self.current_stickers):
            cv2.rectangle(frame, (x,y), (x+30, y+30), state[index], -1)

    def scan_data(self):

        state   = [0,0,0,
                   0,0,0,
                   0,0,0]

        while True:
            _, frame = self.cam.read()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            key = cv2.waitKey(10) & 0xff

            # init certain stickers.
            self.draw_main_stickers(frame)

            for index,(x,y) in enumerate(self.stickers):
                if(index==0):
                    self.counter+=1
                roi          = rgb[y:y+5, x:x+30]
                avg_rgb      = ColorDetector.average_rgb(roi)
                avg_rgb=list(avg_rgb)
                color_line = str(avg_rgb[0])+','+str(avg_rgb[1])+','+str(avg_rgb[2])+','+self.human_color[index]+'\n'
                # print(index, avg_rgb)
                print(index,color_line)
                state[index]=avg_rgb

                if(self.human_color[index]==''):
                    continue
                self.train_data.writelines(color_line)
                if self.counter == self.total:
                    self.train_data.close()
                    break

            self.draw_current_stickers(frame, state)
            # append amount of scanned sides
            text = 'scanned proce: {}/{}'.format(self.counter,self.total)
            cv2.putText(frame, text, (20, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)

            # quit on escape.
            if key == 27:
                self.train_data.close()
                break
            # show result
            cv2.imshow("freecreation", frame)


        self.cam.release()
        cv2.destroyAllWindows()
        # return sides if len(sides) == 6 else False

webcam = Webcam()
webcam.scan_data()
