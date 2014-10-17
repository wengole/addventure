#!/usr/bin/env python

import cv2
import numpy as np
import shelve


def trackChanged(value):
    pass


lower = "Lower"
upper = "Upper"
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

feed = cv2.VideoCapture(0)
cv2.namedWindow("Input")
cv2.namedWindow("Threshold")
cv2.namedWindow("Output")
cv2.namedWindow("Sliders", cv2.WINDOW_NORMAL)

cv2.createTrackbar("Hue_Min", "Sliders", low["h"], 180, trackChanged)
cv2.createTrackbar("Hue_Max", "Sliders", high["h"], 180, trackChanged)
cv2.createTrackbar("Sat_Min", "Sliders", low["s"], 255, trackChanged)
cv2.createTrackbar("Sat_Max", "Sliders", high["s"], 255, trackChanged)
cv2.createTrackbar("Val_Min", "Sliders", low["v"], 255, trackChanged)
cv2.createTrackbar("Val_Max", "Sliders", high["v"], 255, trackChanged)

rval, frame = feed.read()
openingFilter = np.ones((3, 3), np.uint8)

while (True):
    if frame is not None:
        # grey_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lowerH = cv2.getTrackbarPos("Hue_Min", "Sliders")
        upperH = cv2.getTrackbarPos("Hue_Max", "Sliders")
        lowerS = cv2.getTrackbarPos("Sat_Min", "Sliders")
        upperS = cv2.getTrackbarPos("Sat_Max", "Sliders")
        lowerV = cv2.getTrackbarPos("Val_Min", "Sliders")
        upperV = cv2.getTrackbarPos("Val_Max", "Sliders")

        lowerColour = np.array([lowerH, lowerS, lowerV], dtype=np.uint8)
        upperColour = np.array([upperH, upperS, upperV], dtype=np.uint8)

        colourMask = cv2.inRange(hsv_image, lowerColour, upperColour)
        blank_image = np.zeros(frame.shape, np.uint8)
        thresh_image = cv2.bitwise_not(blank_image, blank_image,
                                       mask=colourMask)

        opening = cv2.morphologyEx(colourMask, cv2.MORPH_OPEN, openingFilter)
        masked_image = cv2.bitwise_and(frame, frame, mask=opening)

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
            cv2.circle(frame, (cx, cy), 20, (0, 255, 0))

        cv2.imshow("Input", frame)
        cv2.imshow("Threshold", thresh_image)
        cv2.imshow("Output", masked_image)

    rval, frame = feed.read()
    if cv2.waitKey(10) & 0xFF == ord('q'):
        vals["lowerH"] = lowerH
        vals["lowerS"] = lowerS
        vals["lowerV"] = lowerV

        vals["upperH"] = upperH
        vals["upperS"] = upperS
        vals["upperV"] = upperV
        print("lowerH: ", lowerH)
        print("lowerS: ", lowerS)
        print("lowerV: ", lowerV)
        print("upperH: ", upperH)
        print("upperS: ", upperS)
        print("upperV: ", upperV)

        break

feed.release()
cv2.destroyAllWindows()