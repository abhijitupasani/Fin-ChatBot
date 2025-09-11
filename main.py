from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from db import init_db, get_db
from sqlalchemy.orm import Session
from models import Document, Conversation
from llm_backends import call_llm_hf

app = FastAPI(title="Banking Assistant (MVP)")

@app.on_event("startup")
def on_startup():
    # create tables if not exist
    init_db()

# --- Request models
class AskRequest(BaseModel):
    question: str
    user_id: str | None = None

class UploadRequest(BaseModel):
    title: str | None = None
    content: str

# --- Endpoints
@app.post("/ask")
def ask(req: AskRequest, db: Session = Depends(get_db)):
    # Construct a helpful banking assistant prompt
    prompt = (
        "You are a helpful, concise banking assistant for retail customers. "
        "Answer clearly and step-by-step when asked for workflows. "
        "If the question involves policy and you are uncertain, say you don't have the exact policy and suggest how the user can verify (e.g., visit branch, call support).\n\n"
        f"Question: {req.question}\n\n"
        "Keep the answer short (<= 200 words), actionable, and avoid hallucination."
    )

    try:
        answer = call_llm_hf(prompt, max_tokens=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # store conversation
    conv = Conversation(user_id=req.user_id, question=req.question, answer=answer)
    db.add(conv)
    db.commit()
    db.refresh(conv)

    return {"answer": answer, "conversation_id": conv.id}

@app.post("/upload")
def upload_doc(req: UploadRequest, db: Session = Depends(get_db)):
    # For MVP we just store the content; RAG (chunking + embeddings) will come later
    doc = Document(title=req.title, content=req.content)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"id": doc.id, "title": doc.title}

@app.get("/conversations")
def list_conversations(limit: int = 50, db: Session = Depends(get_db)):
    rows = db.query(Conversation).order_by(Conversation.created_at.desc()).limit(limit).all()
    return [
        {"id": r.id, "user_id": r.user_id, "question": r.question, "answer": r.answer, "created_at": r.created_at}
        for r in rows
    ]

@app.get("/health")
def health():
    return {"status": "ok"}
