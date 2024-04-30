import cv2
from imutils import resize

cap = cv2.VideoCapture('/dev/video0') 

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

success, frame = cap.read()
# frame = resize(frame, width=250)

print(frame.shape[0], frame.shape[1])

while success:
    _, image = cap.read()
    image = resize(image, width=250)
    cv2.imshow("aa", image)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

