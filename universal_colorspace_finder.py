import cv2
from imutils import resize
from camutil import Cam
import numpy as np
from enum import Enum, auto


# cap = cv2.VideoCapture('asset/lotOfBalls/lotOfBalls.mp4')
# cap = cv2.VideoCapture(0)
cam = Cam('topsilo.h264', _isPiCam=True)

class colorspace(Enum):
    hsv = auto()
    yuv = auto()
    hls = auto()

colorSpace = colorspace.yuv

# color = [0, 255, 0, 255, 150, 255]  # hsv
if colorSpace == colorspace.yuv:
    color = [0, 255, 140, 255, 0, 130]  # blue
elif colorSpace == colorspace.hsv:
    color = [0, 255, 0, 255, 170, 255]
elif colorSpace == colorspace.hls:
    color = [0, 255, 0, 255, 170, 255]

def trackBarChanged(value):
    print(f"{color[0]}, {color[1]}, {color[2]}, {color[3]}, {color[4]}, {color[5]}")
    pass


cv2.namedWindow('Trackbars')


cv2.resizeWindow('Trackbars', 600, 250)

# Creat trackbars
cv2.createTrackbar('Huemin', 'Trackbars', color[0], 255, trackBarChanged)
cv2.createTrackbar('Huemax', 'Trackbars', color[1], 255, trackBarChanged)

cv2.createTrackbar('Satmin', 'Trackbars', color[2], 255, trackBarChanged)
cv2.createTrackbar('Satmax', 'Trackbars', color[3], 255, trackBarChanged)

cv2.createTrackbar('Valmin', 'Trackbars', color[4], 255, trackBarChanged)
cv2.createTrackbar('Valmax', 'Trackbars', color[5], 255, trackBarChanged)


while True:
    image = cam.cam_read()
    original = image.copy()
    # image = cv2.imread("asset/12red.jpg")

    image = resize(image, width=250)

    height, width = image.shape[:2]
    image = cv2.GaussianBlur(image, (5, 5), 0)
    # mean_brightness = np.mean(image)
    # if mean_brightness > 127:
    #     image = cv2.convertScaleAbs(image, alpha=1 - (mean_brightness - 127) / 127.0, beta=0)  # Giảm độ sáng
    # else:
    #     image = cv2.convertScaleAbs(image, alpha=1 + (127 - mean_brightness) / 127.0, beta=0)  # Tăng độ sáng

    # image = cv2.imread('./asset/aimBall.jpg')
    
    img_converted = None
    if colorSpace == colorspace.hsv:
        img_converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    elif colorSpace == colorspace.yuv:
        img_converted = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    elif colorSpace == colorspace.hls:
        img_converted = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

    # split image into single chanels
    first, second, third = cv2.split(image)
    grouped = np.concatenate([first, second, third], axis=0)

    # print(len(cv2.split(image)[0]))

    color[0] = cv2.getTrackbarPos('Huemin', 'Trackbars')
    color[1] = cv2.getTrackbarPos('Huemax', 'Trackbars')

    color[2] = cv2.getTrackbarPos('Satmin', 'Trackbars')
    color[3] = cv2.getTrackbarPos('Satmax', 'Trackbars')

    color[4] = cv2.getTrackbarPos('Valmin', 'Trackbars')
    color[5] = cv2.getTrackbarPos('Valmax', 'Trackbars')

    lower = np.array([color[0], color[2], color[4]])
    upper = np.array([color[1], color[3], color[5]])

    mask = cv2.inRange(img_converted, lower, upper)

    # print(type(mask))
    # print(type(image))
    # result = cv2.vconcat([image, mask])

    first, second, third = cv2.split(image)
    grouped = np.concatenate([first, second, third], axis=0)

    imgFin = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    result = np.concatenate([image, imgFin], axis=1)

    # show result
    cv2.imshow('Trackbars', result)
    cv2.imshow('colorspace', grouped)
    # cv2.imshow('hsv', cv2.cvtColor(image, cv2.COLOR_RGB2HSV))

    if cv2.waitKey(40) & 0xFF == ord('q'):
        break

print(f"{color[0]}, {color[1]}, {color[2]}, {color[3]}, {color[4]}, {color[5]}")
cv2.destroyAllWindows()
