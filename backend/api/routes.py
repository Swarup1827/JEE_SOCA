from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import sys
import os

# Get the project root directory
# routes.py is in backend/api/, so go up 3 levels to project root
current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import from backend
from backend import questions, model

router = APIRouter()

# Data Models
class AnalysisRequest(BaseModel):
    user_answers: Dict[str, Dict[str, str]]

# Global model state
ml_model = None
tokenizer = None
device = None

@router.get("/subjects")
async def get_subjects():
    return {"subjects": questions.get_all_subjects()}

@router.get("/questions/{subject}")
async def get_subject_questions(subject: str):
    try:
        # Use shuffle=False to ensure deterministic ordering
        # This is critical for answer key matching in the analyze endpoint
        qs = questions.get_questions(subject, shuffle=False)
        # Strip correct answers for security
        sanitized_questions = []
        for q in qs:
            q_copy = q.copy()
            if "correct_answer" in q_copy:
                del q_copy["correct_answer"]
            sanitized_questions.append(q_copy)
        return {"questions": sanitized_questions}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/analyze")
async def analyze_performance(request: AnalysisRequest):
    global ml_model, tokenizer, device
    
    if not ml_model:
        # Try loading again if failed at startup
        try:
            ml_model, tokenizer, device = model.load_model()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Model not loaded")

    user_answers = request.user_answers
    
    # Reconstruct answer key from questions.py
    # We need the full questions with correct answers
    subjects = questions.get_all_subjects()
    answer_key = {}
    
    # We need to match the question structure expected by model.py
    # model.py expects answer_key[subject][q_no] = {"correct_answer": ..., "question": ...}
    # But questions.py returns a list of questions without IDs.
    # The frontend must send answers keyed by "Q1", "Q2" etc. corresponding to the index.
    
    # IMPORTANT: The original app shuffled questions and stored them in session state.
    # In a stateless API, we have a problem: if we shuffle on every request, the indices won't match.
    # For this migration, to keep it simple, we will NOT shuffle questions in the API for now,
    # OR we rely on the frontend to send the full question text or ID?
    # The original app used `st.session_state.shuffled_questions`.
    
    # Let's look at `questions.py`. `get_questions` shuffles them!
    # This is bad for a stateless API if we want to verify answers by index.
    # We should modify `questions.py` to NOT shuffle by default, or handle it differently.
    
    # For now, let's modify `questions.py` to have a `get_questions(subject, shuffle=False)` option.
    # But wait, `questions.py` logic:
    # def get_questions(subject): ... random.shuffle ...
    
    # I will modify `questions.py` to remove mandatory shuffling or make it optional.
    # And in `routes.py`, we will fetch UNSHUFFLED questions to generate the answer key.
    # The frontend will receive questions. If the frontend wants to shuffle, it can, but it needs to track original IDs.
    # The simplest approach for this migration is:
    # 1. Backend serves questions in FIXED order (or seeded random).
    # 2. Frontend displays them.
    # 3. Frontend sends answers with indices "Q1", "Q2" (1-based index).
    # 4. Backend reconstructs answer key using the SAME FIXED order.
    
    # So I MUST modify `questions.py` to stop shuffling or allow disabling it.
    
    # Let's assume we modify `questions.py` first.
    
    # Constructing answer key based on FIXED order
    for subject in subjects:
        # We need a way to get questions deterministically.
        # I'll assume I've fixed `questions.py` to allow `shuffle=False`.
        qs = questions.get_questions(subject, shuffle=False) 
        answer_key[subject] = {}
        for i, q in enumerate(qs):
            q_key = f"Q{i+1}"
            answer_key[subject][q_key] = {
                "correct_answer": q["correct_answer"],
                "question": q["question"]
            }
            
    # Now generate analysis
    try:
        formatted_text = model.preprocess_responses(user_answers, answer_key)
        analysis = model.generate_soca_analysis(
            ml_model, tokenizer, device, formatted_text, user_answers, answer_key
        )
        return {"analysis": analysis}
    except Exception as e:
        print(f"Error generating analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))
