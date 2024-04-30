from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT

class Cam():
    cap = None
    isPiCam = False

    def __init__(self, id, _isPiCam=False):
        self.isPiCam = _isPiCam
        if not _isPiCam:
            self.cap = VideoCapture(id)
            self.cap.set(CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(CAP_PROP_FRAME_HEIGHT, 720)
        if _isPiCam:
            from picamera2 import Picamera2
            self.cap = Picamera2()
            self.cap.configure(self.cap.create_preview_configuration(
                main={
                    "format": 'RGB888',
                    "size": (1920, 1080)
                }))
            self.cap.start()

    def cam_read(self):
        try:
            if not self.isPiCam:
                return self.cap.read()[1]
            if self.isPiCam:
                return self.cap.capture_array()
        except Exception as e:
            print("CAM EROR", e)
            
        return None

    def cam_release(self):
        if not self.isPiCam:
            self.cap.release()
