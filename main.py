from flask import Flask, render_template, Response
from camera import VideoCamera
import os
import threading
import subprocess

app = Flask(__name__)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index_2.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    global main_process_running, main_process
    if main_process_running:
        # Terminate the main process
        main_process.terminate()
        main_process_running = False
    print("Shutting down gracefully...")
    os._exit(0)  # This will forcefully terminate the application

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
