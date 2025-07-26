from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .resume_parser import process_resume
from .database import init_db, get_all_resumes
from .models import ResumeIn
from typing import List
import uvicorn

app = FastAPI(
    title="AI Resume Analyzer API",
    description="An intelligent resume analysis system powered by AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Resume Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "upload_resume": "/upload_resume/",
            "history": "/history/"
        }
    }

@app.post("/upload_resume/", response_model=dict)
async def upload_resume(
    file: UploadFile = File(..., description="Resume PDF file"),
    jd: str = Form(..., description="Job description text")
):
    """
    Upload a resume PDF file and job description for AI analysis.
    
    - **file**: PDF file containing the resume
    - **jd**: Job description text to match against the resume
    
    Returns detailed analysis including skills, ratings, and improvement suggestions.
    """
    if not file.filename.endswith('.pdf'):
        return JSONResponse(
            status_code=400,
            content={"error": "Only PDF files are allowed"}
        )
    
    result = await process_resume(file, jd)
    return result

@app.get("/history/", response_model=List[dict])
async def get_resume_history():
    """
    Get the history of all processed resumes.
    
    Returns a list of all previously analyzed resumes with their analysis results.
    """
    return await get_all_resumes()

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)