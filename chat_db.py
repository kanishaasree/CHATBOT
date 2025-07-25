import streamlit as st
from google import generativeai as genai
import os
from dotenv import load_dotenv
from chat_db import (
    create_tables, get_all_sessions, get_messages_by_session,
    add_message, delete_session
)
from auth import show_login, show_register

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize database
create_tables()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "email" not in st.session_state:
    st.session_state.email = None
if "current_session" not in st.session_state:
    st.session_state.current_session = None

# Show login/register before anything else
if not st.session_state.logged_in:
    st.sidebar.empty()  # ✅ Hide sidebar during login/register
    auth_mode = st.sidebar.radio("Choose:", ["Login", "Register"])
    if auth_mode == "Login":
        show_login()
    else:
        show_register()
    print("User is logged in:", st.session_state.logged_in)  # ✅ Debugging info
    st.stop()

# ✅ Show user is logged in (just for debug, optional)
print("User is logged in:", st.session_state.logged_in)

# Sidebar - session list and delete
st.sidebar.title("Sessions")
sessions = get_all_sessions(st.session_state.email)

for sess in sessions:
    if st.sidebar.button(sess):
        st.session_state.current_session = sess

    if st.sidebar.button(f"❌ Delete {sess}", key=f"del_{sess}"):
        delete_session(sess, st.session_state.email)
        if st.session_state.current_session == sess:
            st.session_state.current_session = None
        st.rerun()

# Main Chat Interface
st.title("Gemini Chatbot")

if not st.session_state.current_session:
    st.session_state.current_session = st.text_input("Start a new session", "")

if st.session_state.current_session:
    st.subheader(f"Session: {st.session_state.current_session}")
    messages = get_messages_by_session(st.session_state.current_session, st.session_state.email)

    for role, content in messages:
        with st.chat_message(role):
            st.markdown(content)

    if prompt := st.chat_input("You:"):
        # Store user message
        st.chat_message("user").markdown(prompt)
        add_message("user", prompt, st.session_state.current_session, st.session_state.email)

        # Generate response with Gemini
        contents = [{"role": "user", "parts": [prompt]}]
        full_reply = ""
        with st.chat_message("assistant"):
            placeholder = st.empty()
            for chunk in genai.GenerativeModel("gemini-1.5-flash").generate_content_stream(contents):
                full_reply += chunk.text
                placeholder.markdown(full_reply)
        add_message("assistant", full_reply, st.session_state.current_session, st.session_state.email)
