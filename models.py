from pydantic import BaseModel

class ChatRequest(BaseModel): #JSON payload the client sends, containing a user message
    message: str

class ChatResponse(BaseModel): #AI chatbot’s text reply returned from the API
    reply: str

