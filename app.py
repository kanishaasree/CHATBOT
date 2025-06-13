import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from models import Message
from chat_db import create_tables, save_message, get_messages, get_all_sessions
from PIL import Image
import io

# Load API key
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# DB setup
create_tables()

# Streamlit UI setup
st.set_page_config(page_title="Gemini Chatbot", layout="wide")
st.title("Gemini Chatbot")

# Initialize current session
if "current_session" not in st.session_state:
    st.session_state.current_session = "Default Session"
    st.session_state.messages = get_messages("Default Session")

if "image_data" not in st.session_state:
    st.session_state.image_data = None
    st.session_state.image_name = ""

# Sidebar: session switching
st.sidebar.title("Chats")
sessions = get_all_sessions()

def switch_session(session_name):
    st.session_state.current_session = session_name
    st.session_state.messages = get_messages(session_name)

for session in sessions:
    if st.sidebar.button(session, use_container_width=True):
        switch_session(session)

# New session
if st.sidebar.button("\u2795 New chat", use_container_width=True):
    new_session = f"Session {len(sessions) + 1}"
    st.session_state.current_session = new_session
    st.session_state.messages = []

# Upload image (hidden uploader styled like paperclip)
st.sidebar.markdown("<br><b>Attach Image</b>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Upload image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    st.session_state.image_data = uploaded_file.read()
    st.session_state.image_name = uploaded_file.name
    st.sidebar.success(f"Uploaded: {uploaded_file.name}")

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg.role):
        st.markdown(msg.content)

# Input and response
if prompt := st.chat_input("Say something to Gemini!"):
    user_msg = Message(role="user", content=prompt)
    st.session_state.messages.append(user_msg)
    save_message(st.session_state.current_session, user_msg.role, user_msg.content)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_reply = ""

        try:
            # If image was uploaded
            if st.session_state.image_data:
                image = Image.open(io.BytesIO(st.session_state.image_data))
                image_path = f"temp_{st.session_state.image_name}"
                image.save(image_path)
                gemini_file = genai.upload_file(path=image_path)

                response = model.generate_content([gemini_file, prompt], stream=True)

                for chunk in response:
                    full_reply += chunk.text
                    placeholder.markdown(full_reply)

                os.remove(image_path)
                # Clear image after use
                st.session_state.image_data = None
                st.session_state.image_name = ""
            else:
                # No image: plain text conversation
                history_text = ""
                for m in st.session_state.messages:
                    history_text += f"{m.role.capitalize()}: {m.content}\n"
                history_text += f"User: {prompt}\nAssistant:"

                response = model.generate_content(history_text, stream=True)

                for chunk in response:
                    full_reply += chunk.text
                    placeholder.markdown(full_reply)

        except Exception as e:
            st.error(f"Error: {e}")

    bot_msg = Message(role="assistant", content=full_reply)
    st.session_state.messages.append(bot_msg)
    save_message(st.session_state.current_session, bot_msg.role, bot_msg.content)
