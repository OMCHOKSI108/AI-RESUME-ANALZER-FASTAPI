from pydantic import BaseModel
from tortoise.models import Model
from tortoise import fields
from typing import List, Optional

class ResumeIn(BaseModel):
    name: str
    email: str
    core_skills: List[str]
    soft_skills: List[str]
    resume_rating: int
    improvement_areas: str
    uploaded_file_name: str
    job_fit_score: Optional[float] = None
    upskill_suggestions: str
    skillset_improvements: List[str]

class Resume(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100)
    core_skills = fields.JSONField()
    soft_skills = fields.JSONField()
    resume_rating = fields.IntField()
    improvement_areas = fields.TextField()
    uploaded_file_name = fields.CharField(max_length=100)
    job_fit_score = fields.FloatField(null=True)
    upskill_suggestions = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    skillset_improvements = fields.JSONField()  # Added to match ResumeIn