from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str   # frontend sends only message

class ChatResponse(BaseModel):
    reply: str
