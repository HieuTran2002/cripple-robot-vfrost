from flask import Flask, Response, render_template
import cv2
from trackBall import process
from serial_utils import uart
uart = uart()

app = Flask(__name__)
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    print("------- Star View -------")
    while True:
        result, data = process()
        uart.put(data)
        print(data)
        ret, visMe = cv2.imencode('.jpg', result)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + visMe.tobytes() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

