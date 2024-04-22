import cv2
from imutils import resize
from camutil import Cam
import numpy as np

# cap = cv2.VideoCapture('asset/lotOfBalls/lotOfBalls.mp4')
# cap = cv2.VideoCapture(0)
cam = Cam('', _isPiCam=True)
kernel = np.ones((5, 5), np.uint8)


def trackBarChanged(value):
    print(f"{color[0]}, {color[1]}, {color[2]}, {color[3]}, {color[4]}, {color[5]}")


cv2.namedWindow('Trackbars')


cv2.resizeWindow('Trackbars', 600, 250)

# yellow 17 50 200 245 166 251 
# red 0 180 9 104 157 255
# blue 11 103 6 220 143 248
# color = [17, 50, 200, 245, 166, 251] # yellow

# top red  0 180 90 237 216 255

# cam2 red 4 180 0 167 0 255
# cam2 new-purple old-red 54 147 65 255 188 255

color = [71, 160, 56, 255, 122, 255]

# color = [0, 180, 0, 73, 91, 255]

# color = [0, 180, 139, 255, 139, 255]  # old red
# color = [0, 180, 0, 255, 214, 255]  # red with pi camera
# color = [0, 180, 9, 104, 157, 255 ]

cv2.createTrackbar('Huemin', 'Trackbars', color[0], 180, trackBarChanged)
cv2.createTrackbar('Huemax', 'Trackbars', color[1], 180, trackBarChanged)

cv2.createTrackbar('Satmin', 'Trackbars', color[2], 255, trackBarChanged)
cv2.createTrackbar('Satmax', 'Trackbars', color[3], 255, trackBarChanged)

cv2.createTrackbar('Valmin', 'Trackbars', color[4], 255, trackBarChanged)
cv2.createTrackbar('Valmax', 'Trackbars', color[5], 255, trackBarChanged)


while True:
    img = cam.cam_read()
    # img = cv2.imread("asset/12red.jpg")

    img = resize(img, height=500)

    height, width = img.shape[:2]

    # img = cv2.imread('./asset/aimBall.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    cv2.imshow("origin", img)
    # img = img[int(height/2):, int(width/4):-int(width/4)]

    color[0] = cv2.getTrackbarPos('Huemin', 'Trackbars')
    color[1] = cv2.getTrackbarPos('Huemax', 'Trackbars')

    color[2] = cv2.getTrackbarPos('Satmin', 'Trackbars')
    color[3] = cv2.getTrackbarPos('Satmax', 'Trackbars')

    color[4] = cv2.getTrackbarPos('Valmin', 'Trackbars')
    color[5] = cv2.getTrackbarPos('Valmax', 'Trackbars')

    # print(str(hmin) + ', ' + str(hmax) + ', ' +  str(smin) + ', ' + str(smax) + ', ' + str(vmin) + ', ' + str(vmax))

    lower = np.array([color[0], color[2], color[4]])
    upper = np.array([color[1], color[3], color[5]])
    mask = cv2.inRange(img, lower, upper)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    cv2.imshow('Mask', mask)
    # cv2.imshow('hsv', cv2.cvtColor(img, cv2.COLOR_RGB2HSV))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
