import cv2
from datetime import datetime, timedelta
import numpy as np
import scipy

hue_to_find = 333
cap = cv2.VideoCapture(0)
t = datetime.now()
i = 0
while (True):
    i += 1
    if datetime.now() - t > timedelta(seconds=1):
        print i
        i = 0
        t = datetime.now()
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_bound = np.array([0, 0, 250], dtype=np.uint(8))
    upper_bound = np.array([180, 255, 255], dtype=np.uint(8))

    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]
    cX = 0
    cY = 0
    if areas:
        max_index = np.argmax(areas)
        largest = contours[max_index]
        moment = cv2.moments(largest)
        # cX = int(moment['m10'] / moment['m00'])
        # cY = int(moment['m01'] / moment['m00'])
        # cv2.circle(frame, (cX, cY), 4, (0, 255, 0))
        cv2.drawContours(frame, [largest], 0, (0, 255, 0), 3)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('image.png', frame)
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()