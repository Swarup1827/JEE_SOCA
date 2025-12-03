from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any
import os

# Import questions and model from the same directory
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from questions import get_all_subjects, get_questions
    from model import load_model, preprocess_responses, generate_soca_analysis
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback - define minimal functions
    def get_all_subjects():
        return ["Physics", "Chemistry", "Mathematics"]
    def get_questions(subject, shuffle=False):
        return []

app = FastAPI(title="JEE SOCA Analysis API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class AnalysisRequest(BaseModel):
    user_answers: Dict[str, Dict[str, str]]

# Global model state
ml_model = None
tokenizer = None
device = None

@app.get("/")
async def root():
    return {"message": "JEE SOCA API is running", "status": "ok"}

@app.get("/api/subjects")
async def get_subjects():
    try:
        subjects = get_all_subjects()
        return {"subjects": subjects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/questions/{subject}")
async def get_subject_questions(subject: str):
    try:
        qs = get_questions(subject, shuffle=False)
        sanitized_questions = []
        for q in qs:
            q_copy = q.copy()
            if "correct_answer" in q_copy:
                del q_copy["correct_answer"]
            sanitized_questions.append(q_copy)
        return {"questions": sanitized_questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/analyze")
async def analyze_performance(request: AnalysisRequest):
    global ml_model, tokenizer, device
    
    try:
        if not ml_model:
            ml_model, tokenizer, device = load_model()
        
        user_answers = request.user_answers
        subjects = get_all_subjects()
        answer_key = {}
        
        for subject in subjects:
            qs = get_questions(subject, shuffle=False)
            answer_key[subject] = {}
            for i, q in enumerate(qs):
                q_key = f"Q{i+1}"
                answer_key[subject][q_key] = {
                    "correct_answer": q["correct_answer"],
                    "question": q["question"]
                }
        
        formatted_text = preprocess_responses(user_answers, answer_key)
        analysis = generate_soca_analysis(
            ml_model, tokenizer, device, formatted_text, user_answers, answer_key
        )
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Export for Vercel
handler = app
