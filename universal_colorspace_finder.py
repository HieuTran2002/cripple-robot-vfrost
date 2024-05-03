import cv2
from imutils import resize
from camutil import Cam
import numpy as np
from enum import Enum, auto


# cap = cv2.VideoCapture('asset/lotOfBalls/lotOfBalls.mp4')
# cap = cv2.VideoCapture(0)
cam = Cam('/dev/video0', _isPiCam=False)

class colorspace(Enum):
    hsv = auto()
    yuv = auto()
    hls = auto()
    lab = auto()


colorSpace = colorspace.yuv
ball_color = 1
useHSBbackground = True
useHSVbackgroundDouble = False

color = [0] * 6 
color_bg = [0] * 6
color_bg_2 = [0] * 6

# 0, 145, 134, 255, 0, 255

def preset(value):
    global color
    global color_bg
    global ball_color

    ball_color = cv2.getTrackbarPos('ball_color', 'Trackbars')
    
    if colorSpace == colorspace.yuv:
        if ball_color == 2:
            color = [0, 255, 0, 255, 200, 255]  # red
        elif ball_color == 1:
            color = [0, 255, 130, 255, 0, 130]  # blue
    elif colorSpace == colorspace.hsv:
        color = [0, 255, 0, 255, 0, 150]
    elif colorSpace == colorspace.hls:
        color = [0, 255, 0, 255, 170, 255]
    elif colorSpace == colorspace.lab:
        color = [0, 255, 0, 255, 170, 255]
    color_bg = [0,255, 0, 255,0 ,220]


    cv2.setTrackbarPos('Huemin', 'Trackbars', color[0])
    cv2.setTrackbarPos('Huemax', 'Trackbars', color[1])

    cv2.setTrackbarPos('Satmin', 'Trackbars', color[2])
    cv2.setTrackbarPos('Satmax', 'Trackbars', color[3])

    cv2.setTrackbarPos('Valmin', 'Trackbars', color[4])
    cv2.setTrackbarPos('Valmax', 'Trackbars', color[5])

    cv2.setTrackbarPos('Huemin_bg', 'Trackbars', color_bg[0])
    cv2.setTrackbarPos('Huemax_bg', 'Trackbars', color_bg[1])

    cv2.setTrackbarPos('Satmin_bg', 'Trackbars', color_bg[2])
    cv2.setTrackbarPos('Satmax_bg', 'Trackbars', color_bg[3])

    cv2.setTrackbarPos('Valmin_bg', 'Trackbars', color_bg[4])
    cv2.setTrackbarPos('Valmax_bg', 'Trackbars', color_bg[5])


    cv2.setTrackbarPos('ball_color', 'Trackbars', ball_color)
    print(color)


def trackBarChanged(value):
    print(f"{color[0]}, {color[1]}, {color[2]}, {color[3]}, {color[4]}, {color[5]}")
    pass

def decrease_contrast(image, value):
    return cv2.convertScaleAbs(image, alpha=value, beta=0) 

def increase_brightness(image, value):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    hsv = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

cv2.namedWindow('Trackbars')


cv2.resizeWindow('Trackbars', 600, 250)

# Creat trackbars
cv2.createTrackbar('Huemin', 'Trackbars', color[0], 255, trackBarChanged)
cv2.createTrackbar('Huemax', 'Trackbars', color[1], 255, trackBarChanged)

cv2.createTrackbar('Satmin', 'Trackbars', color[2], 255, trackBarChanged)
cv2.createTrackbar('Satmax', 'Trackbars', color[3], 255, trackBarChanged)

cv2.createTrackbar('Valmin', 'Trackbars', color[4], 255, trackBarChanged)
cv2.createTrackbar('Valmax', 'Trackbars', color[5], 255, trackBarChanged)

cv2.createTrackbar('Huemin_bg', 'Trackbars', color_bg[0], 255, trackBarChanged)
cv2.createTrackbar('Huemax_bg', 'Trackbars', color_bg[1], 255, trackBarChanged)

cv2.createTrackbar('Satmin_bg', 'Trackbars', color_bg[2], 255, trackBarChanged)
cv2.createTrackbar('Satmax_bg', 'Trackbars', color_bg[3], 255, trackBarChanged)

cv2.createTrackbar('Valmin_bg', 'Trackbars', color_bg[4], 255, trackBarChanged)
cv2.createTrackbar('Valmax_bg', 'Trackbars', color_bg[5], 255, trackBarChanged)

cv2.createTrackbar('ball_color', 'Trackbars', 1, 2, preset)

preset(0)


while True:
    image = cam.cam_read()
    

    original = image.copy()
    # image = cv2.imread("asset/12red.jpg")

    image = resize(image, width=250)
    image = decrease_contrast(image, 1.2)
    image = increase_brightness(image, 50)
    
    

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
    elif colorSpace == colorspace.lab:
        img_converted = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # split image into single chanels
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    first, second, third = cv2.split(hsv)
    grouped = np.concatenate([first, second, third], axis=0)

    # print(len(cv2.split(image)[0]))

    color[0] = cv2.getTrackbarPos('Huemin', 'Trackbars')
    color[1] = cv2.getTrackbarPos('Huemax', 'Trackbars')

    color[2] = cv2.getTrackbarPos('Satmin', 'Trackbars')
    color[3] = cv2.getTrackbarPos('Satmax', 'Trackbars')

    color[4] = cv2.getTrackbarPos('Valmin', 'Trackbars')
    color[5] = cv2.getTrackbarPos('Valmax', 'Trackbars')

    color_bg[0] = cv2.getTrackbarPos('Huemin_bg', 'Trackbars')
    color_bg[1] = cv2.getTrackbarPos('Huemax_bg', 'Trackbars')

    color_bg[2] = cv2.getTrackbarPos('Satmin_bg', 'Trackbars')
    color_bg[3] = cv2.getTrackbarPos('Satmax_bg', 'Trackbars')

    color_bg[4] = cv2.getTrackbarPos('Valmin_bg', 'Trackbars')
    color_bg[5] = cv2.getTrackbarPos('Valmax_bg', 'Trackbars')

    lower = np.array([color[0], color[2], color[4]])
    upper = np.array([color[1], color[3], color[5]])

    lower_bg = np.array([color_bg[0], color_bg[2], color_bg[4]])
    upper_bg = np.array([color_bg[1], color_bg[3], color_bg[5]])

    lower_bg_2 = np.array([color_bg_2[0], color_bg_2[2], color_bg_2[4]])
    upper_bg_2 = np.array([color_bg_2[1], color_bg_2[3], color_bg_2[5]])
    
    mask = cv2.inRange(img_converted, lower, upper)
    mask_bg = None

    if useHSBbackground:
        hsv_bg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask_bg = cv2.inRange(hsv_bg, lower_bg, upper_bg)
        if ball_color == 1 and useHSVbackgroundDouble:
            mask_bg_2 = cv2.inRange(hsv_bg, lower_bg_2, upper_bg_2)
            mask_bg = cv2.bitwise_or(mask_bg, mask_bg_2)
        mask_result = cv2.bitwise_and(cv2.bitwise_not(mask_bg), mask)


    # print(type(mask))
    # print(type(image))
    # result = cv2.vconcat([image, mask])

    first, second, third = cv2.split(image)
    grouped = np.concatenate([first, second, third], axis=0)

    mask_img_result = cv2.cvtColor(mask_result, cv2.COLOR_GRAY2BGR)
    mask_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    mask_img_bg = cv2.cvtColor(mask_bg, cv2.COLOR_GRAY2BGR)
    result = np.concatenate([image, mask_img, mask_img_bg, mask_img_result], axis=1)

    # show result
    cv2.imshow('Trackbars', result)
    cv2.imshow('colorspace', grouped)
    # cv2.imshow('hsv', cv2.cvtColor(image, cv2.COLOR_RGB2HSV))

    if cv2.waitKey(40) & 0xFF == ord('q'):
        break

print(f"{color[0]}, {color[1]}, {color[2]}, {color[3]}, {color[4]}, {color[5]}")
cv2.destroyAllWindows()
