import cv2

cap = cv2.VideoCapture('/dev/video2') 

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

success, frame = cap.read()
# print(frame.shape[0], frame.shape[1])

while success:
    _, image = cap.read()
    cv2.imshow("aa", image)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
