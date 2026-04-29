# Agnes AI Tutorials — Code

Hands-on Python examples for building with Agnes AI models, including text generation and image generation.

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
| `day1.py` | Chat completion using `agnes-1.5-flash` |
| `day2.py` | Image generation API using `agnes-image-1.2` |

## Run Locally

Install dependencies:

```bash
pip install fastapi uvicorn requests python-dotenv
```

Start the image generation server:

```bash
uvicorn day2:app --reload --port 5001
```

Then open **[http://localhost:5001/docs](http://localhost:5001/docs)** to test the API interactively.

## Test with Postman

Send a `POST` request to `http://localhost:5001/generate-image` with the following JSON body:

```json
{
  "prompt": "A futuristic city skyline at sunset",
  "size": "1024x768",
  "seed": 42
}
```

The response will render the generated image directly in Postman.
