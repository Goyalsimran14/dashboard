import hashlib
import os
import pandas as pd
import datetime
import streamlit as st

USER_FILE = "users.csv"

def init_user_file():
    if not os.path.exists(USER_FILE):
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(USER_FILE, index=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    users = pd.read_csv(USER_FILE)
    hashed = hash_password(password)
    user = users[(users["username"] == username) & (users["password"] == hashed)]
    return not user.empty

def add_user(username, password):
    users = pd.read_csv(USER_FILE)
    if username in users["username"].values:
        return False
    new_user = pd.DataFrame([[username, hash_password(password)]], columns=["username", "password"])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USER_FILE, index=False)
    return True

def check_reminder():
    now = datetime.datetime.now()
    reminder_time = datetime.time(22, 0)  # 10:00 PM
    if now.time() >= reminder_time and "reminder_shown" not in st.session_state:
        st.session_state.reminder_shown = True
        st.warning("⏰ Reminder: Please update your daywise timetable for tomorrow!")
