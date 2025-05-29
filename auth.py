import streamlit as st
import pandas as pd
import hashlib
import os
import random
import string

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

def reset_password(username):
    users = pd.read_csv(USER_FILE)
    if username in users["username"].values:
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        hashed_new_password = hash_password(new_password)
        users.loc[users["username"] == username, "password"] = hashed_new_password
        users.to_csv(USER_FILE, index=False)
        return new_password
    return None

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
                st.session_state.page = "dashboard"
                st.session_state.authenticated = True
                st.session_state.username = username
            else:
                st.error("❌ Invalid login credentials.")