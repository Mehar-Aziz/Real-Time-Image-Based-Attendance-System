import streamlit as st
import pandas as pd
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Get the current date to display today's attendance
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")

# Auto-refresh to update the table every 2 seconds
count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

# Display the attendance data from the CSV
try:
    # Read the CSV file
    df = pd.read_csv(f'Attendance/Attendance_{date}.csv')
    
    # Fill any missing times and statuses (for 'Absent')
    df['TIME'] = df['TIME'].fillna('')
    df['STATUS'] = df['STATUS'].fillna('Absent')
    
    # Filter to keep only the latest entry per person
    df = df.drop_duplicates(subset=['NAME'])
    
    # Add a sequential index column for display
    df.insert(0, 'No.', range(1, len(df) + 1))

    # Display the filtered dataframe in Streamlit
    st.write("### Today's Attendance")
    st.dataframe(df.style.highlight_max(axis=0))

except FileNotFoundError:
    st.write("Attendance file for today not found. Please check if the system has started correctly.")
