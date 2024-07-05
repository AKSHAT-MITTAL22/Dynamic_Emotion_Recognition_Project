import cv2
from model import FacialExpressionModel
import numpy as np
import openpyxl, os
from datetime import datetime

facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = FacialExpressionModel("vgg19_model.json", "vgg19_model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX


current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Define output path
output_dir = './generated'
output_file = 'results.xlsx'
output_path = os.path.join(output_dir, output_file)

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#Create a new excel notebook
workbook = openpyxl.Workbook()
sheet = workbook.active
header = ['Time','Emotion']
sheet.append(header)


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
        # Clean up: remove the stop flag file if it exists

    #Returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        while True:

            _, fr = self.video.read()
            faces = facec.detectMultiScale(fr, 1.3, 5)

            for (x, y, w, h) in faces:
                fc = fr[y:y+h, x:x+w]

                roi = cv2.resize(fc, (48, 48))
                roi = roi/255.0
                pred = model.predict_emotion(roi[np.newaxis, :, :, :])
                
                # Get the current time
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                #store the results in excel sheet
                sheet.append([current_time, pred])
                #workbook.save(f'results_{current_date_time}.xlsx')
                workbook.save(output_path)

                cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
                cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)

            # Check for 'q' key press to stop predictions
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break  

            _, jpeg = cv2.imencode('.jpg', fr)
            return jpeg.tobytes()