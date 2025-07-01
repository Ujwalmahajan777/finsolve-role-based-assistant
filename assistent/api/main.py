# finsolve_assistent/api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from finsolve_assistent.rag_chain import get_rag_chain
from fastapi.middleware.cors import CORSMiddleware

# Allow frontend access (e.g., React, Streamlit)
app = FastAPI(title="FinSolve RAG Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔐 Change this to specific domains in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas
class QueryInput(BaseModel):
    role: str
    question: str

class QueryOutput(BaseModel):
    answer: str

@app.get("/")
def root():
    return {"message": "FinSolve RAG chatbot is running!"}

@app.post("/query", response_model=QueryOutput)
def query_rag_bot(query: QueryInput):
    try:
        chain = get_rag_chain(query.role.lower())
        result = chain.invoke({
            "role": query.role.lower(),
            "question": query.question
        })
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))