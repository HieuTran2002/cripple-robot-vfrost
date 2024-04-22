import cv2
import time


# setup for picamera
from picamera2 import Picamera2
cv2.startWindowThread()
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 320)}))
picam2.start()


prev_frame_time = 0
new_frame_time = 0
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    im = picam2.capture_array()
    im = cv2.flip(im, 0)
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)

    cv2.putText(im, str(fps), (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow("Camera", im)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()
