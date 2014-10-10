import cv2
from datetime import datetime, timedelta
import numpy as np
import scipy


def extract_bright(grey_img, histogram=False):
    """
    Extracts brightest part of the image.
    Expected to be the LEDs (provided that there is a dark background)
    Returns a Thresholded image
    histgram defines if we use the hist calculation to find the best margin
    """
    ## Searches for image maximum (brightest pixel)
    # We expect the LEDs to be brighter than the rest of the image
    [minVal, maxVal, minLoc, maxLoc] = cv2.minMaxLoc(grey_img)
    #return maxLoc
    #print "Brightest pixel val is %d" % maxVal

    # We retrieve only the brightest part of the image
    # Here is use a fixed margin (80%), but you can use hist to enhance this one
    # if 0:
    #     ## Histogram may be used to wisely define the margin
    #     # We expect a huge spike corresponding to the mean of the background
    #     # and another smaller spike of bright values (the LEDs)
    #     hist = grey_histogram(img, nBins=64)
    #     [hminValue, hmaxValue, hminIdx, hmaxIdx] = cv2.GetMinMaxHistValue(hist)
    #     margin = 0  # statistics to be calculated using hist data
    # else:
    margin = 0.8

    thresh = int(maxVal * margin)  # in pix value to be extracted
    #print "Threshold is defined as %d" % (thresh)

    return cv2.threshold(grey_img, thresh, 255, cv2.THRESH_BINARY)

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
    # Get greyscale
    grey_image = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)
    # Increase contrast
    #contrast_image = cv2.multiply(grey_image, np.array(3.0))
    # Threshold
    thresh, thresh_image = cv2.threshold(grey_image, 233, 255, cv2.THRESH_TOZERO)# | cv2.THRESH_OTSU)


    lower_bound = np.array([0, 0, 250], dtype=np.uint(8))
    upper_bound = np.array([180, 255, 255], dtype=np.uint(8))

    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    #contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #areas = [cv2.contourArea(c) for c in contours]
    #cX = 0
    #cY = 0
    """
    if areas:
        max_index = np.argmax(areas)
        largest = contours[max_index]
        moment = cv2.moments(largest)
        # cX = int(moment['m10'] / moment['m00'])
        # cY = int(moment['m01'] / moment['m00'])
        # cv2.circle(frame, (cX, cY), 4, (0, 255, 0))
        cv2.drawContours(frame, [largest], 0, (0, 255, 0), 3)

    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
    """
    _, extracted = extract_bright(grey_image)
    masked = np.bitwise_and(extracted, grey_image)
    cv2.circle(frame, extract_bright(thresh_image), 4, (0, 255, 0))
    cv2.imshow('frame', frame)
    cv2.imshow('frame2', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('image.png', frame)
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

