import streamlit as st
import pandas as pd
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")

count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

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
