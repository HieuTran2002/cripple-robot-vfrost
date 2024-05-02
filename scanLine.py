import cv2
import numpy as np
from math import sqrt
from database import map

color = [0, 255, 120, 255, 0, 255]
lower = np.array([color[0], color[2], color[4]])
upper = np.array([color[1], color[3], color[5]])

devMode = True
gray = (255, 200, 200)
pink = (200, 200, 255)
cyan = (253, 233, 139)
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255, 200, 200)
thickness = 2
lineType = 2


# resolution
frame_width = 250
frame_height = 140

# silo position140
current_silo = 2


def distance(point1, point2):
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def findClosestPoint(points, center):
    if len(points) != 0:
        points = np.array(points)

        # Calculate Euclidean distances
        distances = np.linalg.norm(points - center, axis=1)

        # Find the index of the minimum distance
        closest_index = np.argmin(distances)

        # Retrieve the closest point
        closest_point = tuple(points[closest_index])

        return closest_point
    else:
        return 0


def draw_text(image, text, position):
    return cv2.putText(image, str(text), position, font, fontScale, pink, thickness, lineType)


# def test(image):
#     image = cv2.GaussianBlur(image, (5, 5), 0)

#     img_converted = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
#     mask = cv2.inRange(img_converted, lower, upper)
    
    
#     # gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

#     kernel = np.ones((5,5),np.uint8)
#     mask = cv2.dilate(mask, kernel, iterations = 1)
    
#     cv2.imshow('Detected mask', mask)


#     canny = cv2.Canny(mask, 50, 100)
#     cv2.imshow('Detected canny', canny)

#     lines = cv2.HoughLinesP(canny, 1, np.pi/180, threshold=20, minLineLength=10, maxLineGap=10)
#     if lines is not None:
#         # print(len(lines))
#         for line in lines:
#             x1, y1, x2, y2 = line[0]
#             cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 10)
#     return image

def findSiloPositionBasedOnLazerValue(lazer, color):
    gap = 2
    if (color == 1 and (lazer > map[color][0] + gap or lazer < map[color][4] - gap)) and (color == 2 and (lazer > map[color][4] + gap or lazer < map[color][0] - gap)):
        return None

    for i in range(0, len(map[color])):
        if lazer < map[color][i] + gap and lazer > map[color][i] - gap:
            return i

    return None


def line2silo(image, color, lazer, devMode=False):
    current_silo = findSiloPositionBasedOnLazerValue(lazer, color)

    if current_silo is None:
        return None, None, None, None

    lines = []
    silos = [None] * 5
    highest_y = 0

    # bluring
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # color segmentation
    img_converted = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    mask = cv2.inRange(img_converted, lower, upper)
    cv2.imshow('lines', mask)
    kernel = np.ones((5, 5), np.uint8)
    # mask = cv2.dilate(mask, kernel, iterations=1)

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # contours processing
    for cnt in cnts:
        cnt_area = int(cv2.contourArea(cnt))

        # contour size filtering
        if cnt_area > 50:
            # print(cnt_area)
            # find the high point of the contour
            top = list([cnt[cnt[:, :, 1].argmin()][0]][0])
            x, y, w, h = cv2.boundingRect(cnt)
            # check contour peak height
            if y > 1 and y + h > 30:
                lines.append(top[0])
                if top[1] > highest_y:
                    highest_y = top[1]
                if devMode:
                    cv2.circle(image, (top[0], top[1]), 8, gray, -1)
                    cv2.line(image, (top[0], 0), top, gray, 2)
                    cv2.rectangle(image, (top[0] - 20, 20), (top[0] + 20, top[1]), gray, 2)
                    cv2.rectangle(image, (x, y), (x + w, y + h), (200, 200, 255), thickness=2)
                    cv2.putText(image, str(cnt_area), (x, y), font, fontScale, cyan, thickness, lineType)
                    cv2.drawContours(image, [cnt], -1, (200, 200, 255), 2)  # Vẽ đường viền xanh quanh đối tượng

    centerPoint = 0
    lines = sorted(lines)
    cur_line = 0
    for i in range(0, len(lines)):
        if lines[i] > 100 and lines[i] < 150:
            cur_line = i
            silos[current_silo] = lines[i]
            centerPoint = lines[i]
            break

    n = 0
    for i in range(cur_line, 0, -1):
        n += 1
        if current_silo - n >= 0:
            silos[current_silo - n] = lines[i - 1]

    n = 0
    for i in range(cur_line, len(lines) - 1):
        n += 1
        if current_silo + n < 5:
            silos[current_silo + n] = lines[i + 1]

    # print("line 2 silo :", current_silo, lines, silos)
    if devMode:
        cv2.imshow("line", image)

    return silos, current_silo, centerPoint, highest_y