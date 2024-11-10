import streamlit as st
import pandas as pd
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import os

# Ensure the Attendance directory exists
if not os.path.exists('Attendance'):
    os.makedirs('Attendance')

# Get current date and time for CSV file name
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timeStamp = datetime.fromtimestamp(ts).strftime("%H-%M-%S")

# Auto-refresh every 2 seconds
count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

# Display FizzBuzz logic (just for demonstration)
if count == 0:
    st.write('Count is Zero')
elif count % 3 == 0 and count % 5 == 0:
    st.write('FizzBuzz')
elif count % 3 == 0:
    st.write('Fizz')
elif count % 5 == 0:
    st.write('Buzz')
else:
    st.write(f"Count: {count}")

# Try reading the attendance CSV, create empty DataFrame if not found
try:
    df = pd.read_csv(f'Attendance/Attendance_{date}.csv')
except FileNotFoundError:
    st.write("No attendance recorded for today yet.")
    df = pd.DataFrame(columns=['NAME', 'TIME', 'STATUS'])  # Empty DataFrame with column names

# Display the DataFrame in the app
st.dataframe(df.style.highlight_max(axis=0))
