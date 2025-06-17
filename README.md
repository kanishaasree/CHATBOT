# PROJECT TITLE
 **Gemini-Chatbot:** An AI-Powered Chatbot with Image Support and Chat History

---

### PROJECT DESCRIPTION:
Gemini-Chatbot is an AI-powered conversational application built using Streamlit and Gemini. It allows users to:

- Upload image files along with their prompts.
- Continue conversations with context, without needing to repeat queries.
- View and switch between past chat sessions.
- Rename or delete chat sessions.
- Start new chats with a single click.
- Experience real-time streaming responses powered by Gemini.

---

### TECHNOLOGIES USED:
 - **STREAMLIT:** An open-source Python framework used for building interactive UIs with minimal code. It simplifies app development without needing to dive into HTML or CSS.
 - **GEMINI(Via gen-ai):** A powerful generative AI API provided by Google, used here to build a chatbot with both text and image support. It also supports response streaming for faster user experience.

---

### HOW TO INSTALL AND RUN PROJECT:
- Ensure you have Python installed on your system.
- Clone this repository to your local machine.
  ```bash 
    git clone <repository>
- Open the project folder in your preferred code editor (e.g., VS Code).
-Create a .env file in the root directory to store your Gemini API key:
    ```bash
        API_KEY=your_gemini_api_key
- Navigate to the project directory in your terminal.
- Create virtual environment and activate it:
    ```bash
        python -m venv venv
        venv\Scripts\activate            
- Install the dependancies:
    ```bash
        pip install -r requirements.txt
- Run the application:
    ```bash
        streamlit run app.py        
---

### HOW TO USE THE PROJECT:
- Once the app launches, it will open in your browser.
- Enter your prompt in the input box at the bottom.
- Optionally, upload image files using the upload icon in the input box (only .jpg, .jpeg, .png supported).
- Click "New chat" in the sidebar to start a new session. Your previous sessions will remain available.
- Use the session list on the sidebar to switch between conversations.
- Click the three dots (⋮) next to a session to rename or delete it.

---
