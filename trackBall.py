import cv2
import numpy as np
from imutils import resize
import threading
import time
from minimax_silo import chooseSilo
# from mastermind import mastermind
from scanLine import line2silo
from serial_utils import uart
# from ball import balls
from strategist import strategist, Gamemode

strategist = strategist(gamemode=Gamemode.THREESILO)
uart = uart()

RobotMode = [0, 0, 0, 0, 0]
selectBall = 0
dataUARTSend = [0, 0, 0, 0]
tempBoSilo=10
DaSet = 1

# dev mode
dev_mode = True


# Hàm thực thi cho tiểu trình 1
def thread_Func_Read_UART():
    global RobotMode
    n = 0
    while True:
        b = 0
        n = 0
        while n < 5 and b != 255:
            b = uart.get()
            if b != 255:
                RobotMode[n] = b
            n += 1
            # print("RobotMode: ", RobotMode)


def thread_Func_Write_UART():
    global dataUARTSend
    while True:
        uart.put(dataUARTSend)
        time.sleep(0.03)
        # print(dataUARTSend)


# Tạo các tiểu trình
thread_Read_UART = threading.Thread(target=thread_Func_Read_UART)
thread_Read_UART.start()

thread_Write_UART = threading.Thread(target=thread_Func_Write_UART)
thread_Write_UART.start()

centers = []

frame_width, frame_height = 250, 140  # 640, 360
frame_center_x = int(frame_width / 2)
frame_center_y = int(frame_height / 2)


# find the close ball with the frame's center
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


def track(image, color, cam_angle):
    centers = []
    if cam_angle >= 16:
        contours_size_max = 5000
        contours_size_min = 100  # 5000
    elif cam_angle >= 13:
        contours_size_max = 5000
        contours_size_min = 150
    else:
        contours_size_max = 5000
        contours_size_min = 10
    
    image = cv2.GaussianBlur(image, (5, 5), 0)
    BGR2YUV_frame = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    BGR2HSV_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # HSV nền
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([255, 255, 150])
    mask_HSV = cv2.inRange(BGR2HSV_frame, lower_color, upper_color)
    
    if color == 1:  # blue
        if cam_angle > 13:
            dark_blue = [0, 255, 140, 255, 0, 130]  # blue
        else:
            dark_blue = [0, 255, 140, 255, 0, 120]

        lower_dark_blue = np.array([dark_blue[0], dark_blue[2], dark_blue[4]], dtype=np.uint8)
        upper_dark_blue = np.array([dark_blue[1], dark_blue[3], dark_blue[5]], dtype=np.uint8)
        mask = cv2.inRange(BGR2YUV_frame, lower_dark_blue, upper_dark_blue)
    else:  # 'red'
        if cam_angle > 13:
            # dark_red = [0, 255, 0, 255, 170, 255]
            dark_red = [100, 255, 0, 120, 170, 255]  # 1 4 2024
            
        else:
            dark_red = [0, 255, 0, 125, 167, 247]  # 21 03 2024

        lower_dark_red = np.array([dark_red[0], dark_red[2], dark_red[4]], dtype=np.uint8)
        upper_dark_red = np.array([dark_red[1], dark_red[3], dark_red[5]], dtype=np.uint8)

        mask = cv2.inRange(BGR2YUV_frame, lower_dark_red, upper_dark_red)

    mask = cv2.bitwise_and(cv2.bitwise_not(mask_HSV), mask)
    # cv2.imshow('mask', mask)

    # find contours in the mask and initialize the current
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in cnts:
        cnt_area = int(cv2.contourArea(cnt))
        # print("contour", cnt_area)
        if cnt_area > contours_size_min and cnt_area < contours_size_max:  # Chỉ xem xét các đối tượng có diện tích lớn hơn 100 pixel
            M = cv2.moments(cnt)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                centers.append((cx, cy))

                if dev_mode:
                    cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)  # Vẽ đường viền xanh quanh đối tượng
                    cv2.circle(image, (cx, cy), 5, (0, 255, 255), 10)  # Màu đỏ, đường viền -1 để vẽ hình tròn đậm
    
    if dev_mode:
        imgFin = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        image = np.concatenate((image, imgFin), axis=1)
    return image, centers


def increase_brightness(image, value):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    hsv = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def decrease_contrast(image, value):
    return cv2.convertScaleAbs(image, alpha=value, beta=0)


def analyzeSilos(image, color, vitriRobot):
    tam_silo, current_silo, points = line2silo(image[70:140, :], color, vitriRobot, dev_mode)
    if not tam_silo:
        return image, None, points
    
    image = image[0:80, :]

    possible_silo = []

    contours_size_min = 50
    contours_size_max = 2000
    
    # blur = cv2.GaussianBlur(image, (15, 15), 0)
    BGR2YUV_frame = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    BGR2HSV_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # -------------------------------------------------------
    # Xác định phạm vi màu xanh dương YUV
    lower_color = np.array([0, 140, 0])
    upper_color = np.array([130, 255, 255])
    mask_blue_YUV = cv2.inRange(BGR2YUV_frame, lower_color, upper_color)
    # HSV
    lower_color = np.array([90, 160, 35])
    upper_color = np.array([255, 255, 255])
    mask_blue_HSV = cv2.inRange(BGR2HSV_frame, lower_color, upper_color)

    # Xác định phạm vi màu đỏ YUV
    lower_color = np.array([0, 0, 140])
    upper_color = np.array([255, 255, 255])
    mask_red_YUV = cv2.inRange(BGR2YUV_frame, lower_color, upper_color)

    # Xác định khoảng màu đỏ trong hệ màu HSV
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask_red_HSV_1 = cv2.inRange(BGR2HSV_frame, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask_red_HSV_2 = cv2.inRange(BGR2HSV_frame, lower_red, upper_red)

    mask_red = cv2.bitwise_and(mask_red_HSV_1 + mask_red_HSV_2, mask_red_YUV)
    mask_blue = cv2.bitwise_and(mask_blue_YUV, mask_blue_HSV)

    mask_tam_silo = np.zeros_like(mask_red)
    for t in range(0, len(tam_silo)):
        if tam_silo[t]:
            mask_tam_silo = cv2.line(mask_tam_silo, (tam_silo[t], 0), (tam_silo[t], 140), (255, 255, 255), 50)

    mask_red = cv2.bitwise_and(mask_red, mask_tam_silo)
    mask_blue = cv2.bitwise_and(mask_blue, mask_tam_silo)

    kernel = np.ones((5, 5), np.uint8)
    # mask = cv2.erode(mask, kernel, iterations=0)
    mask_red = cv2.dilate(mask_red, kernel, iterations=1)
    mask_blue = cv2.dilate(mask_blue, kernel, iterations=1)

    mask_ok = np.zeros_like(mask_red)

    # find contours in the mask and initialize the current
    contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if dev_mode:
            cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)
        # print("area RED:", area)
        if area > contours_size_min and area < contours_size_max:  # Chỉ xem xét các đối tượng có diện tích lớn hơn 100 pixel
            cv2.drawContours(mask_ok, [contour], -1, (255), thickness=cv2.FILLED)

    # find contours in the mask and initialize the current
    contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if dev_mode:
            cv2.drawContours(image, [contour], -1, (255, 0, 0), 2)
        # print("area BLUE:", area)
        if area > contours_size_min and area < contours_size_max:  # Chỉ xem xét các đối tượng có diện tích lớn hơn 100 pixel
            cv2.drawContours(mask_ok, [contour], -1, (255), thickness=cv2.FILLED)

    # ---------------------------------------------------
    kernel = np.ones((5, 5), np.uint8)
    mask_ok = cv2.dilate(mask_ok, kernel, iterations=3)

    contours, _ = cv2.findContours(mask_ok, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if y + h > 60 and w > 25:
            possible_silo.append([x, y, w, h])
        
    for t in range(0, len(tam_silo)):
        if tam_silo[t]:
            timDuoc = 0
            for id in range(0, len(possible_silo)):
                x, y, w, h = possible_silo[id]
                if dev_mode:
                    image = cv2.line(image, (tam_silo[t] + 25, 0), (tam_silo[t] + 25, 140), (255, 200, 200), 2)
                    image = cv2.line(image, (tam_silo[t] - 25, 0), (tam_silo[t] - 25, 140), (255, 200, 200), 2)

                if x + w / 2 > tam_silo[t] - 25 and x + w / 2 < tam_silo[t] + 25:
                    if h > 65:
                        strategist.silos_scan[t] = 3
                        timDuoc = 1
                        break
                    elif h > 37:
                        strategist.silos_scan[t] = 2
                        timDuoc = 1
                        break
                    else:
                        strategist.silos_scan[t] = 1
                        timDuoc = 1
                        break
            if not timDuoc:
                strategist.silos_scan[t] = 0
                     
    if dev_mode:
        imgFin = cv2.cvtColor(mask_ok, cv2.COLOR_GRAY2BGR)
        image = np.concatenate((image, imgFin), axis=0)

        # image = cv2.line(image, (0, 140), (640, 140), (255, 200, 200), 2)

    # -------------------------------------------------------
    # chosenSilo = 0
    # chosenSilo1 = 10
    # chosenSilo2 = 10

    # for idx in range(4, vitriRobot, -1):
    #     if silo_count[idx] == 0 and abs(vitriRobot - chosenSilo1) > abs(vitriRobot - idx):
    #         chosenSilo1 = idx
    #     elif(silo_count[idx] == 1):
    #         chosenSilo += 1
    # for idx in range(0, vitriRobot + 1):
    #     if silo_count[idx] == 0 and abs(vitriRobot - chosenSilo1) > abs(vitriRobot - idx):
    #         chosenSilo1 = idx
    #     elif(silo_count[idx] == 1):
    #         chosenSilo += 1

    # if(chosenSilo == 5): # tat ca cac silo deu bang 1
    #     chosenSilo = 9
    # else:
    #     for idx in range(4, vitriRobot, -1):
    #         if silo_count[idx] == 2 and abs(vitriRobot - chosenSilo2) > abs(vitriRobot - idx):
    #             chosenSilo2 = idx

    #     for idx in range(0, vitriRobot + 1):
    #         if silo_count[idx] == 2 and abs(vitriRobot - chosenSilo2) > abs(vitriRobot - idx):
    #             chosenSilo2 = idx

    #     if(chosenSilo2 < 10):
    #         chosenSilo = chosenSilo2
    #     else:
    #         chosenSilo = chosenSilo1

    chosenSilo = strategist.makeDecision(current_silo)

    print("Silo ARRAY:", strategist.silos_scan, chosenSilo)
    # cv2.imwrite(str(silo_count) + ".jpg", image)
    return image, chosenSilo, points


def process(image, devMode=False):
    dev_mode = devMode
    global dataUARTSend
    global selectBall
    global tempBoSilo
    global DaSet
    x = 0
    y = 0

    # print("RobotMode:", RobotMode)
    # kiem tra xem du lieu truyen len co sai hay ko
    image = resize(image, width=frame_width)
    # preset robotmode
    # RobotMode[1] = 9
    # RobotMode[2] = 7
    # RobotMode[0] = 2

    if image is None or RobotMode[0] < 1 or RobotMode[0] > 2:
        print("Robot EROR:")
        return None

    result = image
    # ------------------------------
    if RobotMode[1] == 10:  # reset viec tim bong
        selectBall = 0
        result = image
    elif RobotMode[1] == 9:  # tim bong
        result, centers = track(image, RobotMode[0], RobotMode[2])
        if dev_mode:
            cv2.circle(result, (frame_center_x, frame_center_y), 5, (0, 255, 255), 10)
        
        if selectBall == 0:
            if RobotMode[2] > 16:
                selectBall = findClosestPoint(centers, (frame_center_x, frame_center_y))
            else:
                selectBall = findClosestPoint(centers, (frame_center_x, frame_height))
        else:
            selectBall = findClosestPoint(centers, selectBall)

        if selectBall != 0:
            x = int(selectBall[0])
            y = int(selectBall[1])
            if dev_mode:
                cv2.circle(result, selectBall, 30, (255, 255, 255), 10)

        dataUARTSend = [x, y, 0, 0]

    elif RobotMode[1] == 8:  # tim silo
        result, chosenSilo, centerSiloPoints = analyzeSilos(image, RobotMode[0], RobotMode[3])
        if centerSiloPoints:
            print("silos: ", strategist.silos_self_count, strategist.silos_scan, centerSiloPoints, chosenSilo)
            dataUARTSend = [0, 0, chosenSilo, centerSiloPoints]
        else:
            dataUARTSend = [0, 0, 10, 0]
    
    elif RobotMode[1] < 6:  # tim bo bong
        if RobotMode[1] >= 0 and RobotMode[1] < 5 :
            tempBoSilo = int(RobotMode[1])
            DaSet = 0
        else:
            if DaSet == 0:
                strategist.silos_self_count[tempBoSilo] += 1
                if strategist.silos_self_count[tempBoSilo] > 3:
                    strategist.silos_self_count[tempBoSilo] = 3
                print("Da bo silo", strategist.silos_self_count, tempBoSilo)
                DaSet = 1

    else:
        result = image

    # cv2.putText(result, str(x) + " - " + str(y), (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 3, cv2.LINE_AA)

    # print("TAM:", x, y)
    if dev_mode:
        cv2.imshow("result", result)

    return result

