import os
import httpx
from app.config import OPENAI_API_KEY, MODEL_NAME

# Choose provider: "openrouter" (default) or "openai"
USE_PROVIDER = os.getenv("PROVIDER", "openrouter")

# --- Option A: OpenRouter (default) ---
async def get_response_openrouter(user_id: str, message: str) -> str:
    """
    Call OpenRouter API (free/cheap alternative to OpenAI).
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",  # OpenRouter key
        "Content-Type": "application/json",
    }

    body = {
        "model": MODEL_NAME,  # e.g. "openai/gpt-3.5-turbo" or "mistralai/mistral-7b-instruct"
        "messages": [
            {"role": "system", "content": "You are a helpful virtual banking assistant."},
            {"role": "user", "content": message}
        ],
        "max_tokens": 200,
    }

    async with httpx.AsyncClient() as client:
        r = await client.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"].strip()


# --- Option B: OpenAI (commented out safely) ---
# from openai import OpenAI
# client = OpenAI(api_key=OPENAI_API_KEY)
#
# async def get_response_openai(user_id: str, message: str) -> str:
#     completion = client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[
#             {"role": "system", "content": "You are a helpful virtual banking assistant."},
#             {"role": "user", "content": message}
#         ],
#         max_tokens=200,
#     )
#     return completion.choices[0].message.content.strip()


# --- Unified function ---
async def get_response(user_id: str, message: str) -> str:
    if USE_PROVIDER == "openai":
        # return await get_response_openai(user_id, message)
        return "⚠️ OpenAI API call commented out. Switch PROVIDER to 'openrouter'."
    else:
        return await get_response_openrouter(user_id, message)
