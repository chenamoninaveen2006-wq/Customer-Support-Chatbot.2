# Atlas: Customer Support AI Chatbot

Atlas is an advanced, AI-powered customer support chatbot built using Python, Flask, and the Groq LLM platform. It is designed to handle user queries dynamically, route serious issues to human agents via an escalation system, and provide a premium user experience akin to modern platforms like ChatGPT.

## 🚀 Features

* **Intelligent AI Conversations**: Powered by the Groq API (Llama 3.1) for lightning-fast, highly accurate responses.
* **Multilingual Speech Support**: Built-in voice recognition and Text-to-Speech (TTS) supporting English (🇺🇸), Hindi (🇮🇳), and Telugu (🇮🇳).
* **Modern UI/UX**: 
    * Glassmorphism design and smooth animations
    * Light / Dark Mode toggles
    * Fully featured sidebar with chat history management (Rename, Pin, Delete)
    * Personalized user profiles and nickname settings
    * Clean inline message actions (👍 Helpful, 👎 Not Helpful, 📋 Copy)
* **Secure Authentication**: Supports multiple login methods (Email, Phone, Username) using hashed passwords via `werkzeug.security`.
* **Smart Escalation & Ticketing**: Automatically detects frustrated or angry users and creates support tickets for human agents.
* **Complete Audit Logging**: Stores users, chats, tickets, and feedback securely using a local SQLite database (`database.db`).

---

## 🛠️ Technology Stack

* **Backend**: Python, Flask
* **Database**: SQLite3
* **AI Provider**: Groq API (`llama-3.1-8b-instant`)
* **Frontend**: HTML5, Vanilla JavaScript, CSS3
* **Environment Management**: `python-dotenv`

---

## ⚙️ Setup and Installation

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your machine.

### 2. Clone the Repository
Open your terminal or VS Code and navigate to the project folder.

### 3. Install Dependencies
Run the following command to install the required Python libraries:
```bash
pip install -r requirements.txt
```
*(If `requirements.txt` is missing, ensure you manually install `flask`, `groq`, and `python-dotenv`)*

### 4. Setup Environment Variables
Create a file named `.env` in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant
```

### 5. Run the Application
Start the Flask server:
```bash
python app.py
```

### 6. Access the Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📂 Project Structure

```
├── app.py                     # Main Flask application and routes
├── config.py                  # Configurations and AI system prompts
├── database.db                # SQLite database (auto-generated)
├── modules/
│   ├── conversation_logger.py # DB operations (users, logs, chats)
│   ├── escalation.py          # AI escalation and sentiment logic
│   ├── llm_client.py          # Groq API connection handler
│   └── response_engine.py     # Response formatting and processing
├── templates/
│   ├── chat.html              # Main chat application UI
│   └── welcome.html           # Landing page UI
├── static/
│   └── style.css              # Custom styling and animations
└── .env                       # Environment variables (API Key)
```

---

## 🤝 Usage Guide

1. **Authentication**: New users can Sign Up from the login screen. You can use an email, phone number, or simple username to create your account.
2. **Chatting**: Simply type a message or use the **🎙️ Mic** icon to speak to Atlas. 
3. **Attachments**: Click the **➕** icon next to the input to mockup uploading files or taking photos.
4. **History Management**: Hover over your past chats in the left sidebar and click the **⋮** menu to rename, pin, or delete them.
5. **Profile Settings**: Click the **⚙️ Gear** icon near your name in the top left to set a custom display Nickname!

python app.py
