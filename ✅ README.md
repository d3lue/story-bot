✅ README.md
Place this in the root as well:

# Stoy-Bot

Story Bot is an experimental, AI-powered interactive storytelling engine designed for web browsers. Users co-create a story with AI-driven characters in real-time, choosing the characters, setting the scene, and interacting via text or voice.

---

## 🚀 Features

- AI-powered multi-character storytelling with memory
- Scene and role-based orchestration
- Chat interface via FastAPI + HTML frontend
- SQLite-based story logging
- Secure environment variable handling with `.env`

---

## 📦 Requirements

- Python 3.10+
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- FastAPI
- Uvicorn
- Jinja2
- python-dotenv
- SQLAlchemy (optional if you're logging to SQLite)

---

## 🔧 Installation

```bash
git clone https://github.com/d3lue/story-bot
cd stoybot
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

Create a .env file with your API key:

OPENAI_API_KEY=sk-xxxxx...

Run the server:

uvicorn main:app --reload

Open http://localhost:8000 in your browser.

✨ Credits
Built by Dan Fallshaw using Python, OpenAI, and FastAPI.

⚠️ Disclaimer
All AI interactions are for creative and experimental purposes only. No personal data is stored unless explicitly configured.