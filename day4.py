import os
import json
import requests
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
CHAT_URL = "https://apihub.agnes-ai.com/v1/chat/completions"

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


def stream_response(messages: list):
    payload = {
        "model": "agnes-1.5-flash",
        "messages": messages,
        "stream": True,
    }

    with requests.post(
        CHAT_URL, headers=headers, json=payload, stream=True
    ) as response:
        for line in response.iter_lines():
            if not line:
                continue

            decoded = line.decode("utf-8").removeprefix("data: ")

            if decoded == "[DONE]":
                yield "data: [DONE]\n\n"
                break

            try:
                chunk = json.loads(decoded)
                token = chunk["choices"][0]["delta"].get("content", "")
                if token:
                    yield f"data: {token}\n\n"
            except (json.JSONDecodeError, KeyError, IndexError):
                continue


# No memory — every request is a fresh conversation
@app.post("/chat")
def chat(body: ChatRequest):
    messages = [{"role": "user", "content": body.message}]
    full_reply = ""
    for chunk in stream_response(messages):
        if "DONE" not in chunk:
            full_reply += chunk.removeprefix("data: ").rstrip("\n")

    return {"reply": full_reply}


class MemoryChatRequest(BaseModel):
    session_id: str
    message: str


conversations: dict[str, list] = {}


# With memory — Agnes remembers the full conversation per session
@app.post("/chat/memory")
def chat_with_memory(body: MemoryChatRequest):
    if body.session_id not in conversations:
        conversations[body.session_id] = []

    conversations[body.session_id].append({"role": "user", "content": body.message})

    def stream_and_save():
        full_reply = ""
        for chunk in stream_response(conversations[body.session_id]):
            if "DONE" not in chunk:
                full_reply += chunk.removeprefix("data: ").rstrip("\n")

            yield chunk
        conversations[body.session_id].append(
            {"role": "assistant", "content": full_reply}
        )
        print(conversations)

    return StreamingResponse(stream_and_save(), media_type="text/event-stream")


@app.delete("/chat/memory/{session_id}")
def clear_conversation(session_id: str):
    conversations.pop(session_id, None)
    return {"message": f"Session {session_id} cleared"}
