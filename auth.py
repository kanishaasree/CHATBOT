# auth.py

import streamlit as st
from werkzeug.security import generate_password_hash, check_password_hash
from chat_db import get_user, register_user

def show_login():
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = get_user(email)
        if user and check_password_hash(user["password"], password):
            st.session_state.logged_in = True
            st.session_state.user_id = user["id"]
            st.session_state.user_email = user["email"]
            st.success("Login successful!")
            st.rerun()

        else:
            st.error("Invalid email or password")

def show_register():
    st.subheader("📝 Register")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pass")

    if st.button("Register"):
        hashed = generate_password_hash(password)
        if register_user(email, hashed):
            st.success("Registration successful! Please log in.")
        else:
            st.error("User already exists")
