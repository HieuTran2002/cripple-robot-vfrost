import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

picam2 = Picamera2()
picam2.video_configuration.main.size = (1920, 1080)
picam2.video_configuration.main.format = "RGB888"
picam2.video_configuration.controls.FrameRate = 30.0

encoder = H264Encoder(10000000)

picam2.start_recording(encoder, 'topsilo.h264')
time.sleep(10)
picam2.stop_recording()
