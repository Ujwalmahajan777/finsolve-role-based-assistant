from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from assistent.rag_chain import get_rag_chain

# Allow frontend access (e.g., React, Streamlit)
app = FastAPI(title="FinSolve RAG Chatbot")



# Pydantic schemas to set constraints for input 
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