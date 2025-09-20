from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest, ChatResponse

app = FastAPI()

# CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your React dev URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    user_id = chat_request.user_id
    user_message = chat_request.message
    
    # Replace this with OpenAI/OpenRouter logic
    reply = f"Received from user {user_id}: {user_message}"
    
    return ChatResponse(reply=reply)
