Gemini-Chatbot: An AI-Powered Chatbot with Image Support and Chat History Using Streamlit and Gemini
📌 Project Description
Gemini-Chatbot is an AI-powered conversational application built using Streamlit and Gemini. It supports image uploads (only image files), enables context-aware conversations, and maintains chat history for each session. Users can:

Upload image files along with their prompts.

Continue conversations with context, without needing to repeat queries.

View and switch between past chat sessions.

Rename or delete chat sessions.

Start new chats with a single click.

Experience real-time streaming responses powered by Gemini.

🛠️ Technologies Used
Streamlit: An open-source Python framework used for building interactive UIs with minimal code. It simplifies app development without needing to dive into HTML or CSS.

Gemini (via google-genai): A powerful generative AI API provided by Google, used here to build a chatbot with both text and image support. It also supports response streaming for faster user experience.

🚀 Installation & Setup
Clone this repository

bash
Copy
Edit
git clone <your-repo-url>
Open the project folder in your preferred code editor (e.g., VS Code).

Create a .env file in the root directory to store your Gemini API key:

ini
Copy
Edit
API_KEY=your_gemini_api_key
Navigate to the project directory in your terminal.

Create and activate a virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
Install the dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the application:

bash
Copy
Edit
streamlit run app.py
💬 How to Use the Project
Once the app launches, it will open in your browser.

Enter your prompt in the input box at the bottom.

Optionally, upload image files using the upload icon in the input box (only .jpg, .jpeg, .png supported).

Click "New chat" in the sidebar to start a new session. Your previous sessions will remain available.

Use the session list on the sidebar to switch between conversations.

Click the three dots (⋮) next to a session to rename or delete it.

