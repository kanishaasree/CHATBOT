import streamlit as st
from dotenv import load_dotenv
import os
from google import genai
from uuid import uuid4
from models import Message
from chat_db import create_tables, save_message, get_messages, get_all_sessions
from PIL import Image
from auth import show_login, show_register

# Load .env variables
load_dotenv()
api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)

# DB setup
create_tables()

# Streamlit config
st.set_page_config(page_title="Gemini Chatbot 💬", layout="wide")
st.title("Gemini Chatbot 💬")

# Authentication state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- AUTH ---
auth_mode = st.sidebar.radio("Select", ["Login", "Register"])
if not st.session_state.logged_in:
    if auth_mode == "Login":
        show_login()
    else:
        show_register()
    st.stop()

# Logout
if st.sidebar.button("Logout"):
    for key in ["logged_in", "user_id", "user_email", "current_session", "messages"]:
        st.session_state.pop(key, None)
    st.success("Logged out")
    st.experimental_rerun()

st.caption(f"👤 Logged in as: {st.session_state.user_email}")

# Session setup
if "current_session" not in st.session_state:
    st.session_state.current_session = "Default Session"

sessions = get_all_sessions(st.session_state.user_id)

def switch_session(session_name):
    st.session_state.current_session = session_name
    st.session_state.messages = get_messages(st.session_state.user_id, session_name)

for session in sessions:
    if st.sidebar.button(session, use_container_width=True):
        switch_session(session)

if st.sidebar.button("➕ New Chat", use_container_width=True):
    new_session = f"Session {uuid4().hex[:6]}"
    st.session_state.current_session = new_session
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = get_messages(st.session_state.user_id, st.session_state.current_session)

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg.role):
        st.markdown(msg.content)

# Chat input
prompt = st.chat_input("Say something and/or attach an image", accept_file=True, file_type=["jpg", "jpeg", "png"])

if prompt:
    user_text = prompt.get("text")
    user_files = prompt.get("files")

    with st.chat_message("user"):
        if user_text:
            st.markdown(user_text)
        if user_files:
            for file in user_files:
                st.image(file, caption=file.name)

    # Save user message
    combined_input = user_text if user_text else ""
    st.session_state.messages.append(Message(role="user", content=combined_input))
    save_message(st.session_state.user_id, st.session_state.current_session, "user", combined_input)

    # Gemini response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_reply = ""

        try:
            contents = []
            if user_text:
                contents.append(user_text)
            if user_files:
                for file in user_files:
                    image = Image.open(file)
                    contents.append(image)

            for chunk in client.models.generate_content_stream(
                model="models/gemini-1.5-flash",
                contents=contents
            ):
                full_reply += chunk.text
                placeholder.markdown(full_reply)
        except Exception as e:
            st.error(f"Error: {e}")

        st.session_state.messages.append(Message(role="assistant", content=full_reply))
        save_message(st.session_state.user_id, st.session_state.current_session, "assistant", full_reply)
