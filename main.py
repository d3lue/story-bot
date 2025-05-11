# main.py

# 1) Load .env first, so that os.getenv("OPENAI_API_KEY") actually works.
from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# 2) Now import your orchestrator (which reads that same env var)
from orchestrator.orchestrator_bot import OrchestratorBot

# 3) Optional: quick sanity‐check printout
API_KEY = os.getenv("OPENAI_API_KEY")
print("🔑 OpenAI API key loaded:", "FOUND" if API_KEY else "MISSING")

# 4) Initialize FastAPI
app = FastAPI()

# 5) Static + templates setup
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 6) Instantiate your OrchestratorBot
orchestrator = OrchestratorBot(api_key=API_KEY)

# 7) If you have a database initializer, register it here
from database import init_db
@app.on_event("startup")
async def on_startup():
    init_db()

# 8) Pydantic model for incoming chat messages
class ChatMessage(BaseModel):
    message: str

# 9) Serve your HTML front‐end
@app.get("/", response_class=HTMLResponse)
async def serve_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 10) Chat endpoint
@app.post("/api/chat")
async def chat_endpoint(payload: ChatMessage):
    reply = orchestrator.process_input(payload.message)
    return {"response": reply}
