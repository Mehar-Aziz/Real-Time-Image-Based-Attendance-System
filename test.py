# from sklearn.neighbors import KNeighborsClassifier

# import cv2 
# import pickle
# import numpy as np
# import os
# import csv
# import time
# from datetime import datetime
# from win32com.client import Dispatch

# def speak(str1):
#     speak= Dispatch(('SAPI.SpVoice'))
#     speak.Speak(str1)

# video= cv2.VideoCapture(0)
# facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')


# with open('data/names.pkl', 'rb') as f:
#     Lables = pickle.load(f)
# with open('data/faces_data.pkl', 'rb') as f:
#     FacesTest = pickle.load(f)

# knn = KNeighborsClassifier(n_neighbors = 5)
# knn.fit(FacesTest, Lables)

# imgBackground = cv2.imread('background.png')

# COL_NAMES = ['NAME', 'TIME']

# while True:
#     ret,frame = video.read()
#     gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces=facedetect.detectMultiScale(gray, 1.3, 5)
#     for (x,y,w,h) in faces:
#         crop_img=frame[y:y+h, x:x+w, :]
#         resize_img=cv2.resize(crop_img, (50,50)).flatten().reshape(1,-1)
#         output = knn.predict(resize_img)
#         ts = time.time()
#         date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
#         timeStamp = datetime.fromtimestamp(ts).strftime("%H-%M-%S")
#         exist= os.path.isfile('Attendance/Attendance_' + date + '.csv')
#         cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 1)
#         cv2.rectangle(frame, (x,y),(x+w,y+h), (50,50,255), 2)
#         cv2.rectangle(frame, (x,y-40),(x+w,y), (50,50,255), -1)
#         cv2.putText(frame, str(output[0]),(x,y-15),cv2.FONT_HERSHEY_COMPLEX,1, (255,255,255), 1)
#         cv2.rectangle(frame, (x,y),(x+w,y+h), (50,50,255), 1)
#         attendance = [str(output[0]), str(timeStamp)]
#     imgBackground[175:175 + 480, 115:115 + 640] = frame
#     cv2.imshow("Frame", imgBackground)
#     k=cv2.waitKey(1)
#     if k==ord('o'):
#         speak("Attendace Taken!")
#         time.sleep(2)
#         if exist:
#             with open('Attendance/Attendance_' + date + '.csv', '+a') as csvfile:
#                 writer =csv.writer(csvfile)
#                 writer.writerow(attendance)
#             csvfile.close()
#         else:
#             with open('Attendance/Attendance_' + date + '.csv', '+a') as csvfile:
#                 writer =csv.writer(csvfile)
#                 writer.writerow(COL_NAMES)
#                 writer.writerow(attendance)
#             csvfile.close()
#     if k==ord('q'):
#         break
# video.release()
# cv2.destroyAllWindows()

from sklearn.neighbors import KNeighborsClassifier
import cv2 
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

def speak(str1):
    speak = Dispatch(('SAPI.SpVoice'))
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

# Create the directory if it doesn't exist
if not os.path.exists('Attendance'):
    os.makedirs('Attendance')

# Get the current date and time for marking attendance
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timeStamp = datetime.fromtimestamp(ts).strftime("%H-%M-%S")

# Check if the attendance CSV exists, create it with default 'Absent' status if not
if not os.path.isfile(f'Attendance/Attendance_{date}.csv'):
    with open(f'Attendance/Attendance_{date}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(COL_NAMES)
        # Write all names with 'Absent' status
        for name in Labels:
            writer.writerow([name, "", 'Absent'])

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resize_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resize_img)

        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timeStamp = datetime.fromtimestamp(ts).strftime("%H-%M-%S")

        # Draw rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

        # If the 'o' key is pressed, mark attendance for the recognized person
        if cv2.waitKey(1) & 0xFF == ord('o'):
            speak(f"Attendance Taken for {output[0]}")
            time.sleep(2)

            # Update the CSV with 'Present' status for the recognized person
            attendance_data = []
            with open(f'Attendance/Attendance_{date}.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                attendance_data = list(reader)

            # Update the status for the recognized person
            for row in attendance_data[1:]:
                if row[0] == output[0]:
                    row[2] = 'Present'
                    row[1] = timeStamp

            # Write the updated data back to the CSV
            with open(f'Attendance/Attendance_{date}.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(attendance_data)

        # Display the updated frame with face and name
        imgBackground[175:175 + 480, 115:115 + 640] = frame
        cv2.imshow("Frame", imgBackground)

    # If the 'q' key is pressed, exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
video.release()
cv2.destroyAllWindows()
