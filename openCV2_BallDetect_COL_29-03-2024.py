import cv2
import numpy as np

def increase_brightness(image, value):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    hsv = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def decrease_contrast(image, value):
    return cv2.convertScaleAbs(image, alpha=value, beta=0)

while True:
    # Đọc video từ tệp
    video_path = 'D:/OneDrive/Py/img/silo_left.mp4'
    cap = cv2.VideoCapture(video_path)

    while True:
        # Đọc từng khung hình trong video
        ret, frame = cap.read()
        if not ret:
            break

        new_width = 600  
        ratio = new_width / frame.shape[1]  
        new_height = int(frame.shape[0] * ratio)
        frame = cv2.resize(frame, (new_width, new_height))

        # frame = frame[120:250, 50:550]

        # frame = cv2.GaussianBlur(frame, (5, 5), 0)


        # # Giảm độ tương phản
        # frame = decrease_contrast(frame, 0.3)

        # # # Tăng độ sáng
        # frame = increase_brightness(frame, 50)

        # Chuyển đổi khung hình sang không gian màu HSV
        BGR2YUV_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        BGR2HSV_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        #==============================================================================
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


        kernel = np.ones((5, 5), np.uint8)
        # mask = cv2.erode(mask, kernel, iterations=0)
        mask_red = cv2.dilate(mask_red, kernel, iterations = 1)
        mask_blue = cv2.dilate(mask_blue, kernel, iterations = 1)

        cv2.imshow('mask_red', mask_red)
        cv2.imshow('mask_Blue', mask_blue)

        mask_ok = np.zeros_like(mask_red)

        # find contours in the mask and initialize the current
        contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 300 and area < 5000:  # Chỉ xem xét các đối tượng có diện tích lớn hơn 100 pixel
                cv2.drawContours(mask_ok, [contour], -1, (255), thickness=cv2.FILLED)

        cv2.imshow('mask_ok_RED', mask_ok)

        # find contours in the mask and initialize the current
        contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 300 and area < 5000:  # Chỉ xem xét các đối tượng có diện tích lớn hơn 100 pixel
                cv2.drawContours(mask_ok, [contour], -1, (255), thickness=cv2.FILLED)


        cv2.imshow('mask_ok', mask_ok)

        # # Tìm các đối tượng màu đỏ trong khung hình
        # contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # # Khởi tạo một mask trống có cùng kích thước với ảnh grayscale
        # mask_new = np.zeros_like(mask)

        # for contour in contours:
        #     area = cv2.contourArea(contour)
        #     print("area contour:", area)
        #     approx = cv2.approxPolyDP(contour, 0.03 * cv2.arcLength(contour, True), True)

        #     if area > 10 and area < 99 and len(approx) > 6 and len(approx) < 15:
        #         cv2.drawContours(mask_new, [contour], -1, 255, -1)

        #     if area > 100 and area < 9999:  # Chỉ xem xét các đối tượng có diện tích lớn hơn 100 pixel
        #         # cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)  # Vẽ đường viền xanh quanh đối tượng
        #         M = cv2.moments(contour)
        #         if M['m00'] != 0:
        #             cx = int(M['m10'] / M['m00'])
        #             cy = int(M['m01'] / M['m00'])
        #             cv2.circle(frame, (cx, cy), 3, (0, 255, 255), 3)  # Màu đỏ, đường viền -1 để vẽ hình tròn đậm



        #             # approx = cv2.approxPolyDP(contour, 0.03 * cv2.arcLength(contour, True), True)
                    
        #             # # Số cạnh của đa giác gần đúng
        #             # num_sides = len(approx)
                    
        #             # # Xác định hình dạng dựa trên số cạnh
        #             # shape = ""
        #             # if num_sides == 3:
        #             #     print("------------------------------------------Triangle:", area)
        #             # elif num_sides == 4:
        #             #     cv2.rectangle(frame, (cx- 20, cy- 20), (cx + 20, cy+20), (0, 255, 0), 2)
        #             # elif num_sides == 5:
        #             #     shape = "Pentagon"
        #             #     print("++++++++++++++++++++++++++++++++++++++++Pentagon:", area)
        #             # elif num_sides == 6:
        #             #     print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Hexagon:", area)
        #             # else:
        #             #     cv2.circle(frame, (cx, cy), 20, (0, 255, 255), 3)  # Màu đỏ, đường viền -1 để vẽ hình tròn đậm
                        

        #============================================================
    
        imgFin = cv2.cvtColor(mask_ok, cv2.COLOR_GRAY2BGR)
        vis = np.concatenate((frame, imgFin), axis=0)


        # kernel = np.ones((5, 5), np.uint8)
        # mask_new = cv2.dilate(mask_new, kernel, iterations = 5)

        # cv2.imshow('Result Image', mask_new)

        # Hiển thị khung hình kết quả
        cv2.imshow('Red Ball Detection', vis)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
