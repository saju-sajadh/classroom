import os
import threading
from speechRecognition import record_audio, recognize_speech
from voiceOut import Voice_out
from generativeai import get_response
from face import Face_Recog
from emotion import Emotion_detections
from src.actions import Action_Detection


# Function to run face recognition
def run_face_recognition():
    Face_Recog()

# Function to run emotion detection
def run_emotion_detection():
    Emotion_detections()

def run_action_mode():
    Action_Detection()

# Define the main function
def main():
    current_mode_thread = None
    Voice_out('Program started')
    while True:
        audio = record_audio()
        text = recognize_speech(audio)
        if text.lower() == "hello":
            print("Activated!")
            Voice_out("Hello, what can I do for you?")
            while True:
                audio = record_audio()
                text = recognize_speech(audio)
                if text.lower() == "stop":
                    if current_mode_thread and current_mode_thread.is_alive():
                        Voice_out("Stopping the current mode.")
                        current_mode_thread.do_run = False
                        current_mode_thread.join()
                    break
                elif text.lower() == "activate action mode":
                    Voice_out("Action mode activated!")
                    if current_mode_thread and current_mode_thread.is_alive():
                        current_mode_thread.do_run = False
                        current_mode_thread.join()
                    current_mode_thread = threading.Thread(target=run_action_mode)
                    current_mode_thread.start()
                elif text.lower() == "activate face mode":
                    Voice_out("Face mode activated!")
                    if current_mode_thread and current_mode_thread.is_alive():
                        current_mode_thread.do_run = False
                        current_mode_thread.join()
                    current_mode_thread = threading.Thread(target=run_face_recognition)
                    current_mode_thread.start()
                elif text.lower() == "activate emotion mode":
                    Voice_out("Emotion mode activated!")
                    if current_mode_thread and current_mode_thread.is_alive():
                        current_mode_thread.do_run = False
                        current_mode_thread.join()
                    current_mode_thread = threading.Thread(target=run_emotion_detection)
                    current_mode_thread.start()
                elif text.lower() == "activate chat mode":
                    response = get_response(text)
                    Voice_out(response)
                else:
                    print('not an activation command')
        else:
            print("Not activated.")

if __name__ == "__main__":
    main()
