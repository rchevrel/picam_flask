from threading import Thread, Lock
import io
import picamera
from flask import Flask, render_template, Response
import time

app = Flask(__name__)

camera = picamera.PiCamera()
camera.framerate = 5
#camera.resolution = (2592, 1944) # 640, 480)
#camera.iso = 800

image_mutex = Lock()
image = None

def start_rpicam():
    global image
    stream = io.BytesIO()
    for _ in camera.capture_continuous(stream, 'jpeg'):
        image_mutex.acquire()
        try:
            image = stream.getvalue()
        finally:
            image_mutex.release()
        # next image
        camera.annotate_text = get_current_time()
        stream.seek(0)
        stream.truncate()

def image_gen():
    while True:
        image_mutex.acquire()
        try:
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
        finally:
            image_mutex.release()

def get_current_time() :
    return time.strftime('%d %b %Y %H:%M:%S', time.localtime())

@app.route('/')
def index():
    """Video streaming"""
    return render_template('./index.html')
    
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(image_gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    cam_sync = Thread(target = start_rpicam)
    cam_sync.start()
    app.run(host='0.0.0.0')
