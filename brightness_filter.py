import cv2
from imutils import resize
from camutil import Cam
import numpy as np
from enum import Enum, auto


# cap = cv2.VideoCapture('asset/lotOfBalls/lotOfBalls.mp4')
# cap = cv2.VideoCapture(0)
cam = Cam('/dev/video0', _isPiCam=False)
lower = 0
upper = 0


def trackBarChanged(value):
    print(f"{upper}, {lower}")
    pass


cv2.namedWindow('Trackbars')

cv2.resizeWindow('Trackbars', 600, 250)

# Creat trackbars
cv2.createTrackbar('min', 'Trackbars', 0, 255, trackBarChanged)
cv2.createTrackbar('max', 'Trackbars', 255, 255, trackBarChanged)


while 1:
    image = cam.cam_read()
    image = resize(image, width=250)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    lower = cv2.getTrackbarPos('min', 'Trackbars')
    upper = cv2.getTrackbarPos('max', 'Trackbars')
    
    mask = cv2.inRange(gray, lower, upper)
    cv2.imshow('Trackbars', mask)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
exit()
