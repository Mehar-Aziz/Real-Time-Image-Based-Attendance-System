from sklearn.neighbors import KNeighborsClassifier

import cv2 
import pickle
import numpy as np
import os

video= cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')


with open('data/names.pkl', 'rb') as f:
    Lables = pickle.load(f)
with open('data/faces_data.pkl', 'rb') as f:
    FacesTest = pickle.load(f)

knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(FacesTest, Lables)

imgBackground = cv2.imread('background.png')

while True:
    ret,frame = video.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        crop_img=frame[y:y+h, x:x+w, :]
        resize_img=cv2.resize(crop_img, (50,50)).flatten().reshape(1,-1)
        output = knn.predict(resize_img)
        cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 1)
        cv2.rectangle(frame, (x,y),(x+w,y+h), (50,50,255), 2)
        cv2.rectangle(frame, (x,y-40),(x+w,y), (50,50,255), -1)
        cv2.putText(frame, str(output[0]),(x,y-15),cv2.FONT_HERSHEY_COMPLEX,1, (255,255,255), 1)
        cv2.rectangle(frame, (x,y),(x+w,y+h), (50,50,255), 1)
    imgBackground[175:175 + 480, 115:115 + 640] = frame
    cv2.imshow("Frame", imgBackground)
    k=cv2.waitKey(1)
    if k==ord('q'):
        break
video.release()
cv2.destroyAllWindows()

