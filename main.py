from trackBall import process
from cv2 import imshow, destroyAllWindows, waitKey
from camutil import Cam
import sys


def main(dev_mode):
    cam = Cam('/dev/video0', _isPiCam=False)
    # used to record the time when we processed last frame
    prev_frame_time = 0
    # used to record the time at which we processed current frame
    new_frame_time = 0
    print("Robot Is RUN:")
    while True:
        image = process(cam.cam_read(), dev_mode)
        if image is not None:
            if dev_mode:
                imshow("result", image)
        else:
            print("LOI CAM")
            image = cam.cam_read()
        key = waitKey(1)
        if key == ord('q'):
            break
    destroyAllWindows()
    exit()


if __name__ == "__main__":
    devMode = False
    if len(sys.argv) > 1 and sys.argv[1].lower() in ['true', '1', 'yes']:
        devMode = True
    main(devMode)

