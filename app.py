import streamlit as st
from dotenv import load_dotenv
import os
from google import genai
from models import Message
from chat_db import create_tables, save_message, get_messages, get_all_sessions
from PIL import Image
import io

# Load API key and initialize Gemini client
load_dotenv()
api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)

# DB setup
create_tables()

# Streamlit UI setup
st.set_page_config(page_title="Gemini Chatbot", layout="wide")
st.title("Gemini Chatbot")

# Initialize session state
if "current_session" not in st.session_state:
    st.session_state.current_session = "Default Session"
    st.session_state.messages = get_messages("Default Session")

# Sidebar session control
st.sidebar.title("Chats")
sessions = get_all_sessions()

def switch_session(session_name):
    st.session_state.current_session = session_name
    st.session_state.messages = get_messages(session_name)

for session in sessions:
    if st.sidebar.button(session, use_container_width=True):
        switch_session(session)

if st.sidebar.button("\u2795 New chat", use_container_width=True):
    new_session = f"Session {len(sessions) + 1}"
    st.session_state.current_session = new_session
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg.role):
        st.markdown(msg.content)

prompt = st.chat_input(
    "Say something and/or attach an image",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)

# Process input
if prompt:
    user_text = prompt.get("text")
    user_files = prompt.get("files")

    # Show user's message
    with st.chat_message("user"):
        if user_text:
            st.markdown(user_text)
        if user_files:
            for file in user_files:
                st.image(file, caption=file.name)

    # Save user message
    combined_input = user_text if user_text else ""
    user_msg = Message(role="user", content=combined_input)
    st.session_state.messages.append(user_msg)
    save_message(st.session_state.current_session, user_msg.role, user_msg.content)

    # Generate assistant response
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

            # Generate response with text and/or image
            for chunk in client.models.generate_content_stream(
                model="models/gemini-1.5-flash",
                contents=contents
            ):
                full_reply += chunk.text
                placeholder.markdown(full_reply)

        except Exception as e:
            st.error(f"Error: {e}")

    # Save assistant response
    bot_msg = Message(role="assistant", content=full_reply)
    st.session_state.messages.append(bot_msg)
    save_message(st.session_state.current_session, bot_msg.role, bot_msg.content)
