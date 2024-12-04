import streamlit as st
import pandas as pd
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import cv2
import pickle
import numpy as np
import os

# Streamlit App Setup
st.set_page_config(page_title="Attendance System", layout="wide")

# Navigation Buttons
page = st.sidebar.selectbox("Select Option", ["View Attendance", "Enrollment"])

# Get the current date
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")

# Auto-refresh the page every 2 seconds
count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

# For displaying attendance
if page == "View Attendance":
    try:
        df = pd.read_csv(f'Attendance/Attendance_{date}.csv')
        df['TIME'] = df['TIME'].fillna('')
        df['STATUS'] = df['STATUS'].fillna('Absent')

        df = df.drop_duplicates(subset=['NAME'])
        df.insert(0, 'No.', range(1, len(df) + 1))

        st.write("### Today's Attendance")
        st.dataframe(df.style.highlight_max(axis=0))

    except FileNotFoundError:
        st.write("Attendance file for today not found. Please check if the system has started correctly.")

# For adding faces
elif page == "Enrollment":
    # Input field for name
    name = st.text_input("Enter Roll Number(IN CAPITALS):")

    # Submit button
    if st.button("Submit"):
        if name:
            st.write(f"Capturing faces for {name}...")
            
            video = cv2.VideoCapture(0)
            facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

            faces_data = []
            i = 0

            while True:
                ret, frame = video.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = facedetect.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    crop_img = frame[y:y + h, x:x + w, :]
                    resize_img = cv2.resize(crop_img, (50, 50))
                    if len(faces_data) <= 100 and i % 10 == 0:
                        faces_data.append(resize_img)
                    i += 1
                    cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

                cv2.imshow("Frame", frame)
                k = cv2.waitKey(1)
                if k == ord('q') or len(faces_data) == 100:
                    break

            video.release()
            cv2.destroyAllWindows()

            # Machine learning algorithm
            faces_data = np.asarray(faces_data)
            faces_data = faces_data.reshape(100, -1)

            # names.pkl file creation
            if 'names.pkl' not in os.listdir('data/'):
                names = [name] * 100
                with open('data/names.pkl', 'wb') as f:
                    pickle.dump(names, f)
            else:
                with open('data/names.pkl', 'rb') as f:
                    names = pickle.load(f)
                names = names + [name] * 100
                with open('data/names.pkl', 'wb') as f:
                    pickle.dump(names, f)

            # faces_data.pkl file creation
            if 'faces_data.pkl' not in os.listdir('data/'):
                with open('data/faces_data.pkl', 'wb') as f:
                    pickle.dump(faces_data, f)
            else:
                with open('data/faces_data.pkl', 'rb') as f:
                    faces = pickle.load(f)
                faces = np.append(faces, faces_data, axis=0)
                with open('data/faces_data.pkl', 'wb') as f:
                    pickle.dump(faces, f)

            st.success(f"Face data for {name} has been added successfully.")
        else:
            st.warning("Please enter your name to proceed.")
