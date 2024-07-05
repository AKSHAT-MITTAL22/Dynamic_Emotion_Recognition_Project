from flask import Flask, render_template, Response, send_file, request, jsonify
from camera import VideoCamera
import librosa, numpy as np
# from speech_emotion import EmotionPredictor
from flask_mail import Mail, Message
import os, signal, subprocess,time
from werkzeug.utils import secure_filename
from flask_cors import CORS
import tensorflow as tf
from pydub import AudioSegment
import random

app = Flask(__name__, static_folder='static')
# CORS(app)
# model = tf.keras.models.load_model('speech_cnn_model_weights_new.h5')

# Ensure you have a folder for uploads
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'emotionx.piet@gmail.com'
app.config['MAIL_PASSWORD'] = 'awre mfjs ilbt swub'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# @app.route('/predict_emotion', methods=['POST'])
# def predict_emotion():
#     filename = request.form.get('filename')
#     if not filename:
#         return jsonify({'error': 'Filename not provided'}), 400

#     file_path = os.path.join(UPLOAD_FOLDER, filename)
#     if not os.path.exists(file_path):
#         return jsonify({'error': 'File does not exist'}), 404

#     # Assuming `predictor` is an instance of a class that can handle prediction
#     try:
#         emotion = predictor.predict(file_path)
#         return jsonify({'emotion': emotion})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

emotions = ['Happy', 'Sad', 'Angry', 'Fearful', 'Disgust', 'Surprised', 'Neutral']

@app.route('/predict', methods=['POST'])
def predict():
    audio_file = request.files['audio']
    emotion = random.choice(emotions)
    
    return jsonify(emotion=emotion)


@app.route('/sendFeedback', methods=['POST'])
def send_feedback():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    option = request.form['option']
    message = request.form['message']

    msg = Message("Feedback from " + name,
                  sender=email,
                  recipients=['emotionx.piet@gmail.com'])
    msg.body = f"""
    Name: {name}
    Email: {email}
    Contact No.: {phone}
    Type of Feedback: {option}
    Message: {message}
    """
    mail.send(msg)
    return jsonify({"message": "Feedback sent successfully"}), 200



def gen(camera):
    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/download',methods=['POST'])
def download():
    #Initiate server shutdown process
    #os.kill(os.getpid(), signal.SIGINT)

    # Define the path to your Excel file
    excel_file_path = './generated/results.xlsx'

    return send_file(excel_file_path, as_attachment=True, download_name='emotions_results.xlsx')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def home1():
    return render_template('index.html')

@app.route('/face')
def face_emotion():
    return render_template('face.html')

@app.route('/speech')
def speech_emotion():
    return render_template('speech.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

