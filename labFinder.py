import cv2
import numpy as np
from imutils import resize
from camutil import Cam


cam = Cam('', _isPiCam=True)
# Callback function for trackbar changes
def on_trackbar_change(value):
    # Print LAB threshold values for dark red
    print(f"{lower_dark_red[0]}, {upper_dark_red[0]}, {lower_dark_red[1]}, {upper_dark_red[1]}, {lower_dark_red[2]}, {upper_dark_red[2]}")


kernel = np.ones((5, 5), np.uint8)
# Read your image

# Create a window
cv2.namedWindow('LAB Threshold Adjustments')

# Initial values for LAB thresholds

# dark red: 0, 255, 137, 255, 133, 255
# dark_red = [0, 255, 137, 255, 133, 255]
dark_red = [56, 255, 145, 255, 130, 255]  # merged contours

lower_dark_red = np.array([dark_red[0], dark_red[2], dark_red[4]], dtype=np.uint8)
upper_dark_red = np.array([dark_red[1], dark_red[3], dark_red[5]], dtype=np.uint8)

lower_purple = np.array([30, 60, 60], dtype=np.uint8)
upper_purple = np.array([60, 255, 255], dtype=np.uint8)

lower_dark_blue = np.array([80, 100, 100], dtype=np.uint8)
upper_dark_blue = np.array([130, 255, 255], dtype=np.uint8)

# Create trackbars for LAB thresholds
cv2.createTrackbar('L_min', 'LAB Threshold Adjustments', lower_dark_red[0], 255, on_trackbar_change)
cv2.createTrackbar('L_max', 'LAB Threshold Adjustments', upper_dark_red[0], 255, on_trackbar_change)
cv2.createTrackbar('a_min', 'LAB Threshold Adjustments', lower_dark_red[1], 255, on_trackbar_change)
cv2.createTrackbar('a_max', 'LAB Threshold Adjustments', upper_dark_red[1], 255, on_trackbar_change)
cv2.createTrackbar('b_min', 'LAB Threshold Adjustments', lower_dark_red[2], 255, on_trackbar_change)
cv2.createTrackbar('b_max', 'LAB Threshold Adjustments', upper_dark_red[2], 255, on_trackbar_change)


image = cv2.imread('asset/12032024.jpg')
# cap = cv2.VideoCapture('asset/test.h264')

while 1:
    image = cam.cam_read()
    image = resize(image, width=500)
    # cv2.imwrite('asset/ballNwall.jpg', image)
    # Get current trackbar positions
    lower_dark_red[0] = cv2.getTrackbarPos('L_min', 'LAB Threshold Adjustments')
    upper_dark_red[0] = cv2.getTrackbarPos('L_max', 'LAB Threshold Adjustments')
    lower_dark_red[1] = cv2.getTrackbarPos('a_min', 'LAB Threshold Adjustments')
    upper_dark_red[1] = cv2.getTrackbarPos('a_max', 'LAB Threshold Adjustments')
    lower_dark_red[2] = cv2.getTrackbarPos('b_min', 'LAB Threshold Adjustments')
    upper_dark_red[2] = cv2.getTrackbarPos('b_max', 'LAB Threshold Adjustments')

    lower_purple[0] = cv2.getTrackbarPos('L_min_purple', 'LAB Threshold Adjustments')
    upper_purple[0] = cv2.getTrackbarPos('L_max_purple', 'LAB Threshold Adjustments')
    lower_purple[1] = cv2.getTrackbarPos('a_min_purple', 'LAB Threshold Adjustments')
    upper_purple[1] = cv2.getTrackbarPos('a_max_purple', 'LAB Threshold Adjustments')
    lower_purple[2] = cv2.getTrackbarPos('b_min_purple', 'LAB Threshold Adjustments')
    upper_purple[2] = cv2.getTrackbarPos('b_max_purple', 'LAB Threshold Adjustments')

    lower_dark_blue[0] = cv2.getTrackbarPos('L_min_dark_blue', 'LAB Threshold Adjustments')
    upper_dark_blue[0] = cv2.getTrackbarPos('L_max_dark_blue', 'LAB Threshold Adjustments')
    lower_dark_blue[1] = cv2.getTrackbarPos('a_min_dark_blue', 'LAB Threshold Adjustments')
    upper_dark_blue[1] = cv2.getTrackbarPos('a_max_dark_blue', 'LAB Threshold Adjustments')
    lower_dark_blue[2] = cv2.getTrackbarPos('b_min_dark_blue', 'LAB Threshold Adjustments')
    upper_dark_blue[2] = cv2.getTrackbarPos('b_max_dark_blue', 'LAB Threshold Adjustments')

    # Convert to Lab color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)

    # Create masks for each color
    mask = cv2.inRange(lab_image, lower_dark_red, upper_dark_red)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Combine the masks

    # Apply the combined mask to the original image
    result = cv2.bitwise_and(image, image, mask=mask)

    # Display the result
    # cv2.imshow('LAB Threshold Adjustments', np.hstack([image ,dark_red_mask, result]))
    cv2.imshow('frame', image)
    cv2.imshow('mask ', mask)

    # Break the loop if 'Esc' key is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()

