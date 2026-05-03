# Agnes AI Tutorials — Code

Hands-on Python examples for building with Agnes AI models, including text generation, image generation, and conversational memory.

## Get an API Key

To use any Agnes model, you need an API key.

👉 Generate yours at **[https://platform.agnes-ai.com](https://platform.agnes-ai.com)**

Once you have it, create a `.env` file in this folder:

```
API_KEY=your_api_key_here
```

## Examples

| File | Description |
|---|---|
| `day1.py` | Basic chat completion using `agnes-1.5-flash` |
| `day2.py` | Image generation API using `agnes-image-1.2` (text-to-image) |
| `day3.py` | Image transformation API using `agnes-image-1.2` (image-to-image) |
| `day4.py` | Streaming chat with and without conversational memory |

## Run Locally

Install dependencies:

```bash
pip install fastapi uvicorn requests python-dotenv
```

Start a server:

```bash
uvicorn day2:app --reload --port 5001   # image generation
uvicorn day3:app --reload --port 5002   # image transformation
uvicorn day4:app --reload --port 5003   # streaming chat
```

Then open the interactive docs at `http://localhost:<port>/docs`.

## Test with Postman

### day2 — Generate an image

`POST http://localhost:5001/generate-image`

```json
{
  "prompt": "A futuristic city skyline at sunset",
  "size": "1024x768",
  "seed": 42
}
```

### day3 — Transform an image

`POST http://localhost:5002/transform-image` — use `form-data` body:

| Key | Type | Value |
|---|---|---|
| `prompt` | Text | turn this into a watercolor painting |
| `image` | File | _(select your image file)_ |
| `size` | Text | 1024x1024 _(optional)_ |
| `seed` | Text | 42 _(optional)_ |

### day4 — Chat without memory

`POST http://localhost:5003/chat`

```json
{ "message": "What is Python?" }
```

Returns the full reply as JSON. Agnes has no memory of previous messages.

### day4 — Chat with memory (streaming)

`POST http://localhost:5003/chat/memory`

```json
{ "session_id": "test1", "message": "My name is Ruslan" }
```

Agnes remembers the full conversation per `session_id`. To reset a session:

`DELETE http://localhost:5003/chat/memory/test1`
