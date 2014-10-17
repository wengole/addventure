import shelve
import threading

import cv2
import numpy as np


low = {"h": 0, "s": 0, "v": 0}
high = {"h": 180, "s": 255, "v": 255}

vals = shelve.open("./HSV")
if "lowerH" in vals:
    low["h"] = vals["lowerH"]
    low["s"] = vals["lowerS"]
    low["v"] = vals["lowerV"]
    high["h"] = vals["upperH"]
    high["s"] = vals["upperS"]
    high["v"] = vals["upperV"]

lowerColour = np.array([low["h"], low["s"], low["v"]], dtype=np.uint8)
upperColour = np.array([high["h"], high["s"], high["v"]], dtype=np.uint8)


class WebcamFeed(threading.Thread):

    def __init__(self, **kw):
        threading.Thread.__init__(self, **kw)
        self.feed = cv2.VideoCapture(0)
        self.rval, self.frame = self.feed.read()
        self.openingFilter = np.ones((3, 3), np.uint8)
        self.xOut = 0
        self.yOut = 0

    def run(self):
        while True:
            if self.frame is not None:
                hsv_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
                colourMask = cv2.inRange(hsv_image, lowerColour, upperColour)
                blank_image = np.zeros(self.frame.shape, np.uint8)
                thresh_image = cv2.bitwise_not(blank_image, blank_image,
                                               mask=colourMask)

                opening = cv2.morphologyEx(colourMask, cv2.MORPH_OPEN, self.openingFilter)
                masked_image = cv2.bitwise_and(self.frame, self.frame, mask=opening)

                grey_image = cv2.split(masked_image)[2]

                contours, hierarchy = cv2.findContours(grey_image, cv2.RETR_TREE,
                                                       cv2.CHAIN_APPROX_SIMPLE)
                maxArea = 0
                biggestContour = None

                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > maxArea:
                        biggestContour = contour
                        maxArea = area

                if biggestContour is not None:
                    moment = cv2.moments(biggestContour)
                    cx, cy = int(moment['m10'] / moment['m00']), int(
                    moment['m01'] / moment['m00'])
                    self.xOut = cx
                    self.yOut = cy
            self.rval, self.frame = self.feed.read()

    def join(self, *args, **kw):
        self.feed.release()
        threading.Thread.join(self, *args, **kw)


