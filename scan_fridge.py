'''
Python script for:
1. Taking a webcam capture,
2. Run a object dectection model on the capture
3. Send an email with the detected objects (list & image)

Webcam capture: https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/
Object Detection: https://stackabuse.com/object-detection-with-imageai-in-python/
Email: https://stackabuse.com/how-to-send-emails-with-gmail-using-python/
'''

import cv2
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from imageai.Detection import ObjectDetection

# Model setup
detector = ObjectDetection()

model_path = './yolo-tiny.h5'
input_path = './example.jpeg'
output_path = './newimage.jpg'

detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(model_path)
detector.loadModel()

# Image capture
vid = cv2.VideoCapture(0)
ret, frame = vid.read()
vid.release()
cv2.imwrite(input_path, frame)

# Model inference
detection = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path)
detection_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

# Mail preparation
detection_items = '\n'.join([f"{item['name']}: {item['percentage_probability']}" for item in detection])
print(detection_items)

img_data = open(output_path, 'rb').read()
msg = MIMEMultipart()
msg['Subject'] = 'Fridge update'
msg['From'] = 'claudio.rtega2701@gmail.com'
msg['To'] = 'claudio.rtega2701@gmail.com'

body = MIMEText(f'''
Hola Claudio! Veo que tu refrigeradora tiene los siguientes productos:

{detection_items}

Última lectura: {detection_time}
''')
msg.attach(body)

image = MIMEImage(img_data, name=os.path.basename(output_path))
msg.attach(image)

# Mail sending
gmail_user = 'claudio.rtega2701@gmail.com'
gmail_password = 'Ortega(97)'

try:
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login(gmail_user, gmail_password)
    s.send_message(msg)
    s.close()
    print('Email sent!')
except:
    print('Something went wrong with the email ...')
    raise
