from flask import Flask
from flask import stream_with_context, Response
import picamera

import io
# import picamera

app = Flask(__name__)
camera = picamera.PiCamera()

@app.route("/")
def hello():
    def generate():
        while True:
            stream = io.BytesIO()
            camera.resolution = (640, 480)
            camera.start_recording(stream, format='h264', quality=23)
            camera.wait_recording(1)
            camera.stop_recording()
            yield stream.getvalue()
    # return Response(generate(), direct_passthrough=True)
    return  Response(generate(), mimetype="video/mp4")

# @app.route("/")
# def hello():
#     def generate():
#         with picamera.PiCamera() as camera:
#             while True:
#                 stream = io.BytesIO()
#                 camera.resolution = (640, 480)
#                 camera.start_recording(stream, format='h264', quality=23)
#                 camera.wait_recording(1)
#                 camera.stop_recording()
#                 yield stream.getvalue()
#     # return Response(generate(), direct_passthrough=True)
#     return  Response(stream_with_context(generate()), mimetype="video/mp4")


# @app.route('/stream_data')
# def stream_data():
#     def generate():
#         with open("/root/media_assets/" + file["path"], "rb") as f:
#             while True:
#                 chunk = ... # read each chunk or break if EOF
#                 yield chunk

#     return Response(stream_with_context(generate()), mimetype="video/mp4")
#     # return "Hello World!"



if __name__ == "__main__" and "get_ipython" not in locals():  # ne pas exécuter dans un notebook
    app.run(host='0.0.0.0')