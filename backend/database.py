from tortoise import Tortoise, run_async
import os
from dotenv import load_dotenv
from .models import Resume

load_dotenv()

async def init_db():
    try:
        await Tortoise.init(
            db_url=os.getenv("DATABASE_URL"),
            modules={"models": ["backend.models"]}
        )
        # Generate database schemas
        await Tortoise.generate_schemas()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Database initialization failed: {str(e)}")
        raise

async def insert_resume(data):
    await Resume.create(**data.dict())

async def get_all_resumes():
    try:
        resumes = await Resume.all().order_by("-created_at")
        return [r.__dict__ for r in resumes]
    except Exception as e:
        print(f"Error fetching resumes: {str(e)}")
        raise

if __name__ == "__main__":
    run_async(init_db())