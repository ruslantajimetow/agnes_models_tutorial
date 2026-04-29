import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
IMAGE_URL = "https://apihub.agnes-ai.com/v1/images/generations"

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

app = FastAPI()


class ImageRequest(BaseModel):
    prompt: str
    size: str = "1024x1024"
    seed: int | None = None


@app.post("/generate-image")
def generate_image(body: ImageRequest):
    payload = {
        "model": "agnes-image-1.2",
        "prompt": body.prompt,
        "size": body.size,
    }

    if body.seed is not None:
        payload["seed"] = body.seed

    response = requests.post(IMAGE_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    result = response.json()
    image_url = result.get("data", [{}])[0].get("url")

    image_response = requests.get(image_url)
    content_type = image_response.headers.get("Content-Type", "image/png")

    return Response(content=image_response.content, media_type=content_type)
