import numpy as np
import cv2
import math
import sys
import os
import random
import argparse
from deepface import DeepFace
from collections import deque
import threading
from fer import FER





class Emotion:
    # def __init__(self):
    #     # Initialize the FER detector
    #     self.detector = FER()
    
    # def detect_emotions(self, frame):
    #     # Convert the frame to RGB
    #     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
    #     # Detect emotions
    #     emotions = self.detector.detect_emotions(rgb_frame)
        
    #     for face in emotions:
    #         (x, y, w, h) = face['box']
    #         emotion = face['emotions']
    #         # Get the dominant emotion
    #         dominant_emotion = max(emotion, key=emotion.get)
            
    #         # Draw rectangle around the face and label with emotion
    #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #         cv2.putText(frame, dominant_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
   
    def detect_emotions(self, frame):
        detect_emotion_flag = True if frame.any() else False
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Extract the face ROI (Region of Interest)
            face_roi = rgb_frame[y:y + h, x:x + w]
            if face_roi.shape[0] != 48 or face_roi.shape[1] != 48:
                face_roi = cv2.resize(face_roi, (48, 48))
            if face_roi.shape[2] != 3:
                face_roi = cv2.cvtColor(face_roi, cv2.COLOR_RGB2GRAY)
                face_roi = cv2.cvtColor(face_roi, cv2.COLOR_GRAY2RGB)
            try:
                result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
                emotion = result[0]['dominant_emotion']
                cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            except Exception as e:
                print(f"Error analyzing emotion: {e}")
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)



def Emotion_detections():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        sys.exit("Cannot open camera")

    emotion = Emotion()

    thread = threading.current_thread()

    while getattr(thread, "do_run", True):
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        
        emotion.detect_emotions(frame)

        cv2.imshow('Emotion Detection', frame)  # Show the frame with face recognition

        if cv2.waitKey(1) == 27:  # Press 'ESC' to exit
            break

    cap.release()  # Release the video capture object
    cv2.destroyAllWindows()


# Emotion_detections()