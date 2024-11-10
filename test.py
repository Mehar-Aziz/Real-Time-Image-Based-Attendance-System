from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime, timedelta
from win32com.client import Dispatch

def speak(str1):
    speak = Dispatch('SAPI.SpVoice')
    speak.Speak(str1)

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Load pre-trained names and face data
with open('data/names.pkl', 'rb') as f:
    Labels = pickle.load(f)
with open('data/faces_data.pkl', 'rb') as f:
    FacesTest = pickle.load(f)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FacesTest, Labels)

imgBackground = cv2.imread('background.png')
COL_NAMES = ['NAME', 'TIME', 'STATUS']
attendance_file = f'Attendance/Attendance_{datetime.now().strftime("%d-%m-%Y")}.csv'

# Dictionary to track last attendance times
last_attendance_times = {}

# Initialize attendance CSV if not exists
if not os.path.exists('Attendance'):
    os.makedirs('Attendance')
if not os.path.isfile(attendance_file):
    with open(attendance_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(COL_NAMES)
        for name in Labels:
            writer.writerow([name, "", 'Absent'])

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y + h, x:x + w, :]
        resize_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resize_img)[0]

        current_time = datetime.now()
        last_attendance_time = last_attendance_times.get(output)
        allowed_time = timedelta(hours=1, minutes=30)

        if last_attendance_time is None or (current_time - last_attendance_time) >= allowed_time:
            if cv2.waitKey(1) & 0xFF == ord('o'):
                speak(f"Attendance Taken for {output}")
                last_attendance_times[output] = current_time
                time_stamp = current_time.strftime("%H:%M:%S")

                # Update the attendance in CSV
                with open(attendance_file, 'r') as csvfile:
                    attendance_data = list(csv.reader(csvfile))

                for row in attendance_data[1:]:
                    if row[0] == output:
                        row[1], row[2] = time_stamp, 'Present'
                        break

                with open(attendance_file, 'w', newline='') as csvfile:
                    csv.writer(csvfile).writerows(attendance_data)

        else:
            speak(f"{output}, you cannot mark attendance yet. Please wait.")

        # Draw detected face rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
        cv2.putText(frame, output, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    imgBackground[175:175 + 480, 115:115 + 640] = frame
    cv2.imshow("Frame", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
