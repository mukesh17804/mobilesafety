import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
import psutil
import threading
import time
import winsound
import pyttsx3
import speech_recognition as sr
from sklearn.ensemble import RandomForestRegressor, IsolationForest

class ChargingSafetyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Charging Safety System with AI")
        self.root.geometry("500x400")
        
        self.is_charging = False
        self.is_emergency_mode = False
        self.blocked_window = None
        self.emergency_timer = None
        self.voice_engine = pyttsx3.init()
        
        self.emergency_contact1 = tk.StringVar(value="Not Set")
        self.emergency_contact2 = tk.StringVar(value="Not Set")
        
        self.status_label = tk.Label(root, text="Device is not charging.", font=("Arial", 16))
        self.status_label.pack(pady=20)

        tk.Label(root, text="Emergency Contact 1:").pack()
        tk.Entry(root, textvariable=self.emergency_contact1, width=30).pack(pady=5)
        
        tk.Label(root, text="Emergency Contact 2:").pack()
        tk.Entry(root, textvariable=self.emergency_contact2, width=30).pack(pady=5)

        self.save_button = tk.Button(root, text="Save Contacts", command=self.save_contacts, bg="blue", fg="white")
        self.save_button.pack(pady=10)
        
        self.voice_button = tk.Button(root, text="Voice Assistant", command=self.voice_assistant, bg="green", fg="white")
        self.voice_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app, bg="gray", fg="white")
        self.exit_button.pack(pady=10)
        
        self.monitor_thread = threading.Thread(target=self.monitor_battery_status, daemon=True)
        self.monitor_thread.start()

        self.train_ai_models()

        # Initialize face recognition
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_data = "face_data.xml"  # Pre-trained face data file
        
        try:
            self.recognizer.read(self.face_data)
        except:
            print("Face recognition data not found. Please register face data.")
        
        self.face_recognition_thread = threading.Thread(target=self.face_recognition, daemon=True)
        self.face_recognition_thread.start()

    def train_ai_models(self):
        """Train AI models for Battery Health Prediction and Anomaly Detection."""
        self.battery_model = RandomForestRegressor(n_estimators=100, random_state=42)
        data = np.array([[100, 100, 35, 95], [200, 90, 37, 90], [300, 80, 40, 85], [400, 70, 42, 80], [500, 60, 45, 75]])
        self.battery_model.fit(data[:, :3], data[:, 3])
        
        self.anomaly_detector = IsolationForest(contamination=0.2)
        charging_data = np.array([[4.2, 1.5, 35], [4.1, 1.4, 36], [4.5, 3.0, 50], [4.0, 1.3, 34], [3.9, 2.5, 45]])
        self.anomaly_detector.fit(charging_data)

    def predict_battery_health(self, cycles, charge, temp):
        return self.battery_model.predict([[cycles, charge, temp]])[0]

    def detect_anomaly(self, voltage, charge_rate, temp):
        return self.anomaly_detector.predict([[voltage, charge_rate, temp]])[0] == -1

    def face_recognition(self):
        """Recognize authorized faces before charging is allowed."""
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                face_id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                if confidence < 100:  # If the face is recognized
                    self.speak("Authorized face detected. Charging allowed.")
                else:
                    self.speak("Unrecognized face detected. Charging blocked.")
                    self.block_interface()
            time.sleep(2)
        cap.release()

    def voice_assistant(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.speak("Listening for command.")
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            if "battery" in command:
                battery = psutil.sensors_battery()
                self.speak(f"Your current battery level is {battery.percent} percent.")
            elif "charging" in command:
                battery = psutil.sensors_battery()
                self.speak("Your device is charging." if battery.power_plugged else "Your device is not charging.")
        except Exception:
            self.speak("Sorry, I could not understand that.")

    def monitor_battery_status(self):
        while True:
            battery = psutil.sensors_battery()
            if battery:
                if battery.power_plugged:
                    if not self.is_charging:
                        self.is_charging = True
                        self.block_interface()
                        self.speak_battery_level(battery.percent)
                else:
                    if self.is_charging:
                        self.is_charging = False
                        self.unblock_interface()
                if battery.percent < 20 and self.is_charging:
                    self.show_emergency_button()
            time.sleep(5)

    def block_interface(self):
        self.status_label.config(text="Device is charging. Interface is blocked!", fg="blue")
        if not self.blocked_window:
            self.blocked_window = tk.Toplevel(self.root)
            self.blocked_window.geometry("800x600")
            self.blocked_window.attributes("-fullscreen", True)
            tk.Label(self.blocked_window, text="Device is charging. Unplug to continue.", font=("Arial", 20), fg="red").pack(pady=20)

    def save_contacts(self):
        contact1 = self.emergency_contact1.get()
        contact2 = self.emergency_contact2.get()
        messagebox.showinfo("Contacts Saved", f"Emergency Contact 1: {contact1}\nEmergency Contact 2: {contact2}")

    def speak(self, text):
        self.voice_engine.say(text)
        self.voice_engine.runAndWait()

    def speak_battery_level(self, battery_level):
        self.speak(f"The current battery level is {battery_level} percent. Charging is active.")

    def exit_app(self):
        if self.blocked_window:
            self.blocked_window.destroy()
        if self.emergency_timer:
            self.emergency_timer.cancel()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChargingSafetyApp(root)
    root.mainloop()