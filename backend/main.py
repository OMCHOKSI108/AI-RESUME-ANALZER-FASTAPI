from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.resume_parser import process_resume
from backend.database import init_db, get_all_resumes
import uvicorn

app = FastAPI()

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

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile, jd: str = Form(...)):
    result = await process_resume(file, jd)
    return result

@app.get("/history/")
async def get_resume_history():
    return await get_all_resumes()

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)