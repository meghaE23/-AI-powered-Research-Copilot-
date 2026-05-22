from fastapi.middleware.cors import CORSMiddleware
from ai_utils import summarize_text
from fastapi import FastAPI, UploadFile, File
from pdf_utils import extract_text_from_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Research Copilot Backend Running 🚀"}


paper_text = ""

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global paper_text
    text = extract_text_from_pdf(file.file)
    paper_text = text
    return {"message": "PDF uploaded successfully"}

@app.get("/summary")
def get_summary():
    summary = summarize_text(paper_text)
    return {"summary": summary} 

@app.get("/check")
def check():
    return {"length": len(paper_text)}


from pydantic import BaseModel
from ai_utils import summarize_text

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(q: Question):
    global paper_text
    
    if not paper_text:
        return {"answer": "Please upload a PDF first."}

    # combine question + paper
    prompt = f"Answer this question based on the research paper:\n\n{paper_text[:3000]}\n\nQuestion: {q.question}"

    answer = summarize_text(prompt)

    return {"answer": answer} # first 1000 chars only