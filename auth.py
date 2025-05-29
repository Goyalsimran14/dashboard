import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt  
import random
import hashlib
import sqlite3

# Set Streamlit page configuration
st.set_page_config(page_title="GATE CSE Dashboard", layout="wide")

# Initialize SQLite database
DB_FILE = "dashboard.db"

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "auth"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "subject_progress" not in st.session_state:
    st.session_state.subject_progress = {}
if "study_log" not in st.session_state:
    st.session_state.study_log = []
if "attempted_tests" not in st.session_state:
    st.session_state.attempted_tests = {}
if "course_status" not in st.session_state:
    st.session_state.course_status = {}

# Initialize database
def init_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    # Create study_log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        subject TEXT,
        hours REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_database()

# Hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verify credentials
def verify_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Add new user
def add_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Reset password (send new password)
def reset_password(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
        new_password = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
        hashed_new_password = hash_password(new_password)
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_new_password, username))
        conn.commit()
        conn.close()
        return new_password
    conn.close()
    return None

# Submit study log
def submit_study_log(username, subject, hours, date):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO study_log (username, subject, hours, date) VALUES (?, ?, ?, ?)", (username, subject, hours, date))
    conn.commit()
    conn.close()

# Retrieve study logs
def get_study_logs(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT subject, hours, date FROM study_log WHERE username = ?", (username,))
    logs = cursor.fetchall()
    conn.close()
    return logs

# Authentication function
def authenticate():
    st.title("🔒 Login or Sign Up")
    auth_mode = st.radio("Choose Mode", ["Login", "Sign Up"], horizontal=True)
    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")
    if auth_mode == "Sign Up":
        confirm_password = st.text_input("✅ Confirm Password", type="password")
    submitted = st.button("🔓 Login" if auth_mode == "Login" else "📝 Sign Up")

    if submitted:
        if auth_mode == "Sign Up":
            if password != confirm_password:
                st.error("❌ Passwords do not match.")
            elif not username or not password:
                st.error("⚠️ All fields are required.")
            else:
                if add_user(username, password):
                    st.success("✅ Account created! Please login now.")
                else:
                    st.warning("❌ Username already exists. Try another one.")
        else:
            if verify_user(username, password):
                st.success(f"🎉 Welcome back, {username}!")
                st.session_state.page = "home"
                st.session_state.authenticated = True
                st.session_state.username = username
            else:
                st.error("❌ Invalid login credentials.")

# Placeholder functions for page routing
def home_page():
    st.write("Welcome to the Home Page!")

def dashboard_page():
    st.write("Welcome to the Dashboard Page!")

def daywise_timetable_page():
    st.write("Welcome to the Daywise Timetable Page!")

def weekwise_timetable():
    st.write("Welcome to the Weekwise Timetable Page!")

def notes_section():
    st.write("Welcome to the Notes Section!")

def weekly_pie_chart():
    st.write("Welcome to the Weekly Pie Chart Page!")

def new_page():
    st.write("Welcome to the New Page!")

# Page Routing
if st.session_state.page == "auth":
    authenticate()
elif st.session_state.page == "home":
    home_page()
elif st.session_state.page == "dashboard":
    dashboard_page()
elif st.session_state.page == "daywise":
    daywise_timetable_page()
elif st.session_state.page == "weekwise":
    weekwise_timetable()
elif st.session_state.page == "notes":
    notes_section()
elif st.session_state.page == "pie_chart":
    weekly_pie_chart()
elif st.session_state.page == "new_page":
    new_page()
else:
    st.error("Page not found. Please navigate using the sidebar.")

# Footer
year = datetime.datetime.now().year
st.markdown(f"<hr><footer style='text-align:center; color:gray; font-size:12px;'>© {year} GATE CSE Dashboard | Made with ❤️ by You</footer>", unsafe_allow_html=True)