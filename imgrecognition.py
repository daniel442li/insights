import pytesseract
from PIL import Image
from imutils import contours

import numpy as np
import cv2

imgpath = 'Receipt1.png'

preimg = cv2.imread(imgpath)
gray = cv2.cvtColor(preimg, cv2.COLOR_BGR2GRAY)

preimg = cv2.GaussianBlur(preimg, (1, 1), 0)
kernel = np.ones((5, 5), np.uint8)

img = cv2.blur(preimg, (2, 2), 0)
img = cv2.dilate(img, kernel, iterations= 1)
img = cv2.erode(img, kernel, iterations = 1)

#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts, _ = contours.sort_contours(cnts, method = "left-to-right")

ROI_number = 0

for c in cnts:
    area = cv2.contourArea(c)
    if area > 150:
        x, y, w, h = cv2.boundingRect(c)
        ROI = 255 -img[y:y+h, x:x+w]
        cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
        cv2.rectangle(img,(x, y), (x+w, y+h), (36, 255,12), 1)
        ROI_number += 1

f = open("out.txt", "w+")
f.write(pytesseract.image_to_string(Image.open(imgpath)))



