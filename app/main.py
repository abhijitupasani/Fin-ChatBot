import os
from fastapi import FastAPI, HTTPException
from .models import ChatRequest, ChatResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing only; later restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    user_message = chat_request.message

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=200  # optional: control cost/response length
        )
        # Access reply safely
        reply = response.choices[0].message.content.strip() if response.choices else "No response from model."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenRouter API error: {str(e)}")

    return ChatResponse(reply=reply)
