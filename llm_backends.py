import os
import requests
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")
HUGGINGFACE_MODEL = os.environ.get("HUGGINGFACE_MODEL", "google/flan-t5-large")

if not HUGGINGFACE_API_KEY:
    # we'll raise at call time with a helpful message
    pass

HF_API_URL = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"} if HUGGINGFACE_API_KEY else {}

def call_llm_hf(prompt: str, max_tokens: int = 200) -> str:
    """
    Call HuggingFace Inference API (hosted model).
    Returns a string reply, or raises RuntimeError on error.
    """
    if not HUGGINGFACE_API_KEY:
        raise RuntimeError("HUGGINGFACE_API_KEY is not set. Create a token at HuggingFace and add it to your .env")

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": 0.2,
        },
        # "options": {"wait_for_model": True}  # optional
    }
    try:
        resp = requests.post(HF_API_URL, headers=HEADERS, json=payload, timeout=30)
    except Exception as e:
        raise RuntimeError(f"HuggingFace request failed: {e}")

    if resp.status_code != 200:
        # include response text to help debugging (rate limits, model offline, etc.)
        raise RuntimeError(f"HuggingFace API error {resp.status_code}: {resp.text}")

    data = resp.json()
    # HF returns different shapes depending on model and pipeline; be robust:
    if isinstance(data, dict) and data.get("error"):
        raise RuntimeError(f"HuggingFace error: {data.get('error')}")
    # If model returns a list of dicts with 'generated_text':
    if isinstance(data, list):
        first = data[0]
        if isinstance(first, dict) and "generated_text" in first:
            return first["generated_text"]
        # sometimes it's a plain string inside the list
        if isinstance(first, str):
            return first
        # fallback to stringifying
        return str(data)
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"]
    return str(data)
