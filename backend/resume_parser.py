import PyPDF2 as pdf
from google.generativeai import GenerativeModel
import google.generativeai as genai
import os, json, io, re
from .models import ResumeIn, Resume
from .database import insert_resume
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_text_from_pdf(file):
    reader = pdf.PdfReader(file)
    text = "\n".join([page.extract_text() or "" for page in reader.pages])
    return text if text.strip() else "No text extracted"

def create_fallback_analysis(file, jd):
    """Create a basic analysis when API is unavailable"""
    return {
        "name": "Demo Analysis",
        "email": "demo@example.com",
        "core_skills": ["Python", "FastAPI", "API Development"],
        "soft_skills": ["Communication", "Problem Solving", "Teamwork"],
        "resume_rating": 75,
        "improvement_areas": "API quota exceeded - demo analysis provided. Enhance technical skills and add more project experience.",
        "uploaded_file_name": file.filename,
        "job_fit_score": 70,
        "upskill_suggestions": "Consider upgrading API plan for detailed analysis. Focus on relevant technologies mentioned in job description.",
        "skillset_improvements": ["Advanced programming", "Domain expertise", "Certification courses"]
    }

async def process_resume(file: UploadFile, jd: str):
    content = await file.read()
    text = extract_text_from_pdf(io.BytesIO(content))

    model = GenerativeModel("models/gemini-1.5-flash")  # Changed to lighter model with higher quota

    prompt = f"""
Act as a professional Applicant Tracking System (ATS). Return ONLY clean JSON with a formal tone, NO markdown, NO triple backticks, NO extra text. Use null for missing values and empty lists for missing arrays. Include the following structure exactly as specified:

{{
  "name": "Full name of the candidate",
  "email": "Professional email address",
  "core_skills": ["List", "of", "technical", "skills"],
  "soft_skills": ["List", "of", "soft", "skills"],
  "resume_rating": Integer between 0 and 100,
  "improvement_areas": "Formal summary of areas needing enhancement",
  "uploaded_file_name": "{file.filename}",  // Must use this exact filename
  "job_fit_score": Integer between 0 and 100,
  "upskill_suggestions": "Detailed recommendations for skill development",
  "skillset_improvements": ["Specific", "skill", "areas", "to", "work", "on"]
}}

Resume:
{text}

Job Description:
{jd}
"""

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()
        raw = re.sub(r"```(?:json)?\n?", "", raw).strip()
        raw = re.sub(r"[\n\r\t]+", " ", raw)
        
        if not raw.startswith("{") or not raw.endswith("}"):
            raise json.JSONDecodeError("Invalid JSON format", raw, 0)
        
        parsed = json.loads(raw)
        
        # Override uploaded_file_name with the actual filename
        parsed["uploaded_file_name"] = file.filename
        # Ensure job_fit_score has a default value
        parsed.setdefault("job_fit_score", 0)

        # Ensure all required fields are present with defaults
        parsed.setdefault("name", "Unknown Candidate")
        parsed.setdefault("email", "unknown@default.com")
        parsed.setdefault("core_skills", [])
        parsed.setdefault("soft_skills", [])
        parsed.setdefault("resume_rating", 0)
        parsed.setdefault("improvement_areas", "No specific areas identified.")
        parsed.setdefault("upskill_suggestions", "No specific suggestions at this time.")
        parsed.setdefault("skillset_improvements", [])

        # Validate with Pydantic model
        resume_data = ResumeIn(**{k: v for k, v in parsed.items() if k in ResumeIn.model_fields})
        await insert_resume(resume_data)
        return resume_data.dict(exclude_unset=True)
    except Exception as e:
        # Handle API quota errors specifically
        if "ResourceExhausted" in str(e) or "quota" in str(e).lower():
            # Use fallback analysis when quota is exceeded
            try:
                fallback_data = create_fallback_analysis(file, jd)
                resume_data = ResumeIn(**fallback_data)
                await insert_resume(resume_data)
                return {
                    **resume_data.dict(exclude_unset=True),
                    "warning": "API quota exceeded - using fallback analysis",
                    "message": "Upgrade to paid plan for AI-powered analysis"
                }
            except Exception as fallback_error:
                return {
                    "error": "API quota exceeded and fallback failed",
                    "error_type": "quota_exceeded",
                    "message": "Please wait for quota reset or upgrade your plan",
                    "uploaded_file_name": file.filename,
                    "fallback_error": str(fallback_error)
                }
        elif "json" in str(e).lower():
            return {
                "error": f"JSON parsing failed: {str(e)}", 
                "error_type": "json_error",
                "uploaded_file_name": file.filename,
                "raw_response": locals().get('raw', 'No response received')
            }
        else:
            return {
                "error": f"Processing failed: {str(e)}", 
                "error_type": "general_error",
                "uploaded_file_name": file.filename
            }