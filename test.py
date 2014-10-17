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
    print i
    if datetime.now() - t > timedelta(seconds=1):
        i = 0
        t = datetime.now()
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_pink = np.array([150, 0, 0], dtype=np.uint(8))
    upper_pink = np.array([170, 255, 255], dtype=np.uint(8))

    mask = cv2.inRange(hsv_image, lower_pink, upper_pink)
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    largest = contours[max_index]
    moment = cv2.moments(largest)
    cX = int(moment['m10'] / moment['m00'])
    cY = int(moment['m01'] / moment['m00'])

    cv2.circle(frame, (cX, cY), 4, (0, 255, 0))

    #res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.drawContours(frame, [largest], 0, (0, 255, 0), 3)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('image.png', frame)
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()