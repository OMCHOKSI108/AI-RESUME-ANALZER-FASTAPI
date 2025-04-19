# 🤖 AI Resume Parser ATS System

An end-to-end AI-powered Resume Parsing and Job Fit Analyzer using **Gemini Pro**, **FastAPI**, **Streamlit**, and **PostgreSQL**.

Built with ❤️ by **Om Choksi**  
GitHub: [OMCHOKSI108](https://github.com/OMCHOKSI108)

---

## 📌 Features

- 🧠 Powered by Google Gemini Pro (LLM)
- 📥 Upload your resume and job description (JD)
- ✅ Get structured JSON: name, email, core skills, soft skills, ratings, suggestions, and more
- 🔍 Smart suggestions for upskilling and improvement
- 🗂 View and search all previously uploaded resumes
- 🧾 Clean two-tab UI (Live Analysis + Resume History)
- 💾 Resume data stored in PostgreSQL database
- 🦾 Ready for deployment (Docker, Render, etc.)

---

## 📁 Project Structure

```
ai_resume_parser/
├── backend/
│   ├── main.py               # FastAPI app
│   ├── resume_parser.py      # LLM + Resume Logic
│   ├── models.py             # ORM & Pydantic Models
│   ├── database.py           # DB Connection
│   └── utils.py              # PDF / file utils
│
├── frontend/
│   ├── app.py                # Streamlit Frontend
│   └── assets/               # Optional UI assets
│
├── sample_data/              # Sample resumes for testing
├── screenshots/              # Screenshots for submission
├── .env                      # API key and DB config
├── requirements.txt          # Python dependencies
└── README.md                 # You're here
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/OMCHOKSI108/ai_resume_parser.git
cd ai_resume_parser
```

---

### 2. Setup Python Environment

```bash
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create a `.env` file in the root:

```
GOOGLE_API_KEY=your_gemini_api_key
DATABASE_URL=postgres://resume_user:sans@localhost:5432/resume_final
```

---

### 4. Create PostgreSQL Database

In psql or pgAdmin:

```sql
CREATE DATABASE resume_final;
CREATE USER resume_user WITH PASSWORD 'sans';
GRANT ALL PRIVILEGES ON DATABASE resume_final TO resume_user;
```

---

### 5. Run Backend API (FastAPI)

```bash
cd backend
uvicorn main:app --reload
```

---

### 6. Run Frontend UI (Streamlit)

In a new terminal:

```bash
cd frontend
streamlit run app.py
```

---

## 🧪 Sample Data

Put your test resumes in the `/sample_data/` folder.

---

## 📸 Screenshots

Screenshots of both tabs (Upload + History) are available in `/screenshots/`.

---

## 📚 Tech Stack

- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Gemini](https://deepmind.google/technologies/gemini/)
- [PostgreSQL](https://www.postgresql.org/)
- [Tortoise ORM](https://tortoise-orm.readthedocs.io/)

---

## 🧑‍💻 Author

**Om Choksi**  
GitHub: [OMCHOKSI108](https://github.com/OMCHOKSI108)  
Email: (Add yours here)

---

## 🌟 License

MIT License – free to use with attribution.

```
