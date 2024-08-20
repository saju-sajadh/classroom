import serial
import time
import threading
from speechRecognition import record_audio, recognize_speech
from voiceOut import Voice_out
from generativeai import get_response
from face import Face_Recog
from emotion import Emotion_detections
from src.actions import Action_Detection

# Initialize serial communication with Arduino
arduino = serial.Serial('COM3', 9600)  # Update 'COM3' to your Arduino port

# Define color commands
def send_color_to_arduino(r, g, b):
    command = f"c,{r},{g},{b}\n"
    arduino.write(command.encode())

# Define mode commands
def send_mode_to_arduino(mode):
    if mode == "action":
        arduino.write(b'a')
        send_color_to_arduino(0, 255, 0)  # Green for action mode
    elif mode == "face":
        arduino.write(b'f')
        send_color_to_arduino(0, 0, 255)  # Blue for face mode
    elif mode == "emotion":
        arduino.write(b'e')
        send_color_to_arduino(255, 0, 0)  # Red for emotion mode
    elif mode == "stop":
        arduino.write(b's')
        send_color_to_arduino(0, 0, 0)    # Turn off RGB strip

# Function to run face recognition
def run_face_recognition():
    send_mode_to_arduino("face")
    Face_Recog()
    send_mode_to_arduino("stop")  # Turn off LED when done

# Function to run emotion detection
def run_emotion_detection():
    send_mode_to_arduino("emotion")
    Emotion_detections()
    send_mode_to_arduino("stop")  # Turn off LED when done

def run_action_mode():
    send_mode_to_arduino("action")
    Action_Detection()
    send_mode_to_arduino("stop")  # Turn off LED when done

# Define the main function
def main():
    current_mode_thread = None

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
                    send_mode_to_arduino("stop")
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
                else:
                    response = get_response(text)
                    Voice_out(response)
        else:
            print("Not activated.")

if __name__ == "__main__":
    main()
