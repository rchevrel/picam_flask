#!/usr/bin/env python
from flask import Flask, render_template, Response
import picamera
import socket
import io
# from fractions import Fraction

app = Flask(__name__)

nigth_mode = False
if nigth_mode:
        camera = picamera.PiCamera(
                        resolution=(1296, 730), sensor_mode=5)
                        # framerate=Fraction(1, 6),

        # camera.shutter_speed = 6000000
        camera.iso = 800
        # sleep(30)
        camera.exposure_mode = 'off'
else:
        camera = picamera.PiCamera()
        camera.resolution = (1640, 1232)
        # camera.resolution = (1296, 730)
        # camera.resolution = (3280, 2464)
        camera.iso = 800
        camera.annotate_text = 'Hello world!'
        # camera.rotation = 90

@app.route('/')
def index():
    """Video streaming"""
    return render_template('./index.html')

def gen():
    """Video streaming generator function."""
    stream = io.BytesIO()
    for _ in camera.capture_continuous(stream, 'jpeg'):
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + stream.getvalue() + b'\r\n')
        # camera.annotate_text = 'Hello world!'
        stream.seek(0)
        stream.truncate()

generator = gen()
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(generator,
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)
               
