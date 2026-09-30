from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests

app = FastAPI()


# =========================
# HTML 파일 위치
# =========================

HTML_PATH = r"C:\mococo\index.html"


# =========================
# 채팅 데이터 형식
# =========================

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


# =========================
# 메인 화면
# =========================

@app.get("/")
def home():
    return FileResponse(HTML_PATH)


# =========================
# Qwen 채팅
# =========================

@app.post("/chat")
def chat(data: ChatRequest):

    messages = []

    for message in data.messages:
        messages.append({
            "role": message.role,
            "content": message.content
        })

    response = requests.post(
        "http://127.0.0.1:11434/api/chat",

        json={
            "model": "qwen3:4b",
            "messages": messages,
            "stream": False
        },

        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return {
        "reply": result["message"]["content"]
    }