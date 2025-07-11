from fastapi import FastAPI, UploadFile, File, HTTPException
from app.kb_manager import (
    add_knowledge,
    search_knowledge,
    load_kb_from_file,
    get_knowledge_base,
    extract_text_from_url,
    extract_text_from_pdf,
    extract_text_from_docx
)
from app.models import KBUrlInput, QueryInput
from app.agent import agent

app = FastAPI()
load_kb_from_file() 

@app.post("/add_kb_file")
async def add_kb_file(file: UploadFile = File(...)):
    if file.filename.endswith('.pdf'):
        content = extract_text_from_pdf(file.file)
    elif file.filename.endswith('.docx'):
        content = extract_text_from_docx(file.file)
    else:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")
    add_knowledge(file.filename, content)
    return {"message": "File content added to knowledge base."}

@app.post("/add_kb_url")
async def add_kb_url(input: KBUrlInput):
    content = extract_text_from_url(str(input.url))  # <--- ensure string
    add_knowledge(str(input.url), content)           # <--- ensure string
    print(f"Added URL content: {content[:100]}...")
    return {"message": "URL content added to knowledge base."}

@app.get("/search_kb")
def search_kb(q: str):
    results = search_knowledge(q)
    return {"results": results}

@app.post("/ask")
def ask_agent(query: QueryInput):
    answer = agent.answer(query.question, query.knowledge_only)
    return {"answer": answer}

@app.get("/debug_kb")
def debug_kb():
    return {"knowledge_base": get_knowledge_base()}