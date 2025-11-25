import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_model():
    """
    Configures the Gemini API.
    Returns the configured genai module (acting as the 'model' object).
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Warning: GOOGLE_API_KEY not found in environment variables.")
        return None, None, None
    
    # Configure with REST transport to avoid gRPC/DNS issues
    genai.configure(api_key=api_key, transport="rest")
    model = genai.GenerativeModel('gemini-2.0-flash')
    return model, None, None

def preprocess_responses(user_answers, answer_key):
    try:
        core_subjects = ["Physics", "Chemistry", "Mathematics"]
        non_core_subjects = ["Well-being Assessment", "Time Management"]
        
        formatted_responses = """Student Response Analysis:\n\n"""
        
        # Process Core Subjects
        formatted_responses += "--- ACADEMIC PERFORMANCE ---\n"
        for subject in core_subjects:
            if subject in user_answers:
                formatted_responses += f"\nSubject: {subject}\n"
                questions = user_answers[subject]
                for q_no, user_ans in questions.items():
                    subject_key = answer_key.get(subject, {})
                    q_data = subject_key.get(q_no, {})
                    
                    correct_ans = q_data.get("correct_answer", "Unknown")
                    question_text = q_data.get("question", "")
                    
                    status = "Correct ✅" if user_ans == correct_ans else "Incorrect ❌"
                    formatted_responses += f"{q_no}. {question_text}\n   Your Answer: ({user_ans}), Correct Answer: ({correct_ans}) - {status}\n"

        # Process Non-Core Subjects
        formatted_responses += "\n--- WELL-BEING & TIME MANAGEMENT ---\n"
        for subject in non_core_subjects:
            if subject in user_answers:
                formatted_responses += f"\nSection: {subject}\n"
                questions = user_answers[subject]
                for q_no, user_ans in questions.items():
                    subject_key = answer_key.get(subject, {})
                    q_data = subject_key.get(q_no, {})
                    
                    # For well-being, "correct_answer" is treated as the "Ideal Habit"
                    ideal_ans = q_data.get("correct_answer", "Unknown")
                    question_text = q_data.get("question", "")
                    
                    formatted_responses += f"{q_no}. {question_text}\n   Your Answer: ({user_ans}), Ideal Habit: ({ideal_ans})\n"

        return formatted_responses
    except Exception as e:
        print(f"Error preprocessing responses: {str(e)}")
        raise

def generate_soca_analysis(model, tokenizer, device, user_text, user_answers, answer_key):
    """
    Generates SOCA analysis using Google Gemini API.
    """
    try:
        if not model:
            return "Error: Google API Key not configured. Please add GOOGLE_API_KEY to .env file."

        # Calculate performance metrics
        subject_performance = {}
        for subject, questions in user_answers.items():
            subject_key = answer_key.get(subject, {})
            correct_count = 0
            total = 0
            
            for q_no, ans in questions.items():
                total += 1
                if ans == subject_key.get(q_no, {}).get("correct_answer"):
                    correct_count += 1
            
            if total > 0:
                subject_performance[subject] = (correct_count / total) * 100
            else:
                subject_performance[subject] = 0

        # Create prompt
        prompt = f"""
        You are an expert JEE exam counselor. Analyze these student responses and provide a detailed SOCA (Strengths, Opportunities, Challenges, Action Plan) analysis.
        
        Performance Summary:
        {', '.join(f'{subject}: {score:.1f}%' for subject, score in subject_performance.items())}

        Detailed Responses:
        {user_text}

        Provide a detailed analysis in the following Markdown format:
        
        # 📊 Comprehensive JEE Preparation Analysis

        ## 1. 📚 Subject-wise Performance Distribution
        [Provide a detailed breakdown of performance in Physics, Chemistry, and Mathematics. Highlight specific weak and strong topics based on the questions answered.]

        ## 2. 🧠 Subject-wise SOCA Analysis
        
        ### ⚛️ Physics
        *   **Strengths**: ...
        *   **Opportunities**: ...
        *   **Challenges**: ...
        *   **Action Plan**: ...

        ### 🧪 Chemistry
        *   **Strengths**: ...
        *   **Opportunities**: ...
        *   **Challenges**: ...
        *   **Action Plan**: ...

        ### 📐 Mathematics
        *   **Strengths**: ...
        *   **Opportunities**: ...
        *   **Challenges**: ...
        *   **Action Plan**: ...

        ## 3. 🧘 Well-being & Time Management Review
        [Analyze the student's responses to the Well-being and Time Management sections. Provide specific advice on stress management, sleep, and study scheduling based on their answers.]

        ## 4. 📝 Final Personalized Action Plan
        1. **Immediate Focus**: [Action item]
        2. **Study Strategy**: [Action item]
        3. **Resource Usage**: [Action item]
        
        Keep the tone encouraging but realistic. Focus on actionable advice for JEE preparation.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Error generating analysis with Gemini: {str(e)}")
        return f"Error generating analysis. Please try again. Details: {str(e)}"