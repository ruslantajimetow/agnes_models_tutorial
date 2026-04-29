import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = "https://apihub.agnes-ai.com/v1/chat/completions"

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def first_question():
    messages_data = {
        "model": "agnes-1.5-flash",
        "messages": [{"role": "user", "content": "what is javascript?"}],
    }

    response = requests.post(API_URL, headers=headers, json=messages_data)
    result = response.json()
    print(result)
    print("Agnes says: ", result["choices"][0]["message"]["content"])


first_question()
