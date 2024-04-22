from trackBall import process
from cv2 import imshow, destroyAllWindows, waitKey
from camutil import Cam

cam = Cam('../asset/test.h264', _isPiCam=True)
devMode = False

# used to record the time when we processed last frame
prev_frame_time = 0
  
# used to record the time at which we processed current frame
new_frame_time = 0
print("Robot Is RUN:")
while True:
    image = process(cam.cam_read(), devMode)
    # print(data)

    # fps
    # new_frame_time = time()
    # fps = 1 / (new_frame_time - prev_frame_time)
    # prev_frame_time = new_frame_time
    # fps = str(int(fps))
    # putText(image, fps, (10, 30), FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 3, LINE_AA)

    if image is not None:
        # print("fps", fps)
        if devMode:
            imshow("result", image)
        pass
    else:
        print("LOI CAM")
        image = cam.cam_read()

    key = waitKey(1)
    if key == ord('q'):
        break

destroyAllWindows()
