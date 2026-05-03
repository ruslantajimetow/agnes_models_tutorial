import os
import base64
import requests
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import Response
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
IMAGE_URL = "https://apihub.agnes-ai.com/v1/images/generations"

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

app = FastAPI()


@app.post("/transform-image")
async def transform_image(
    prompt: str = Form(...),
    image: UploadFile = File(...),
    size: str = Form("1024x1024"),
    seed: int | None = Form(None),
):
    image_bytes = await image.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    payload = {
        "model": "agnes-image-1.2",
        "prompt": prompt,
        "extra_body": {
            "image": [
                image_b64,
            ],
            "response_format": "url",
        },
        "size": size,
    }

    if seed is not None:
        payload["seed"] = seed

    response = requests.post(IMAGE_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return {"error": response.text}

    result = response.json()
    image_url = result.get("data", [{}])[0].get("url")

    image_response = requests.get(image_url)
    content_type = image_response.headers.get("Content-Type", "image/png")

    return Response(content=image_response.content, media_type=content_type)
