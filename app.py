import streamlit as st
import model
import json
from typing import Dict, Any
import questions
import random

# Set page config
st.set_page_config(
    page_title="JEE Aspirant SOCA Analysis",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .analysis-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .subject-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    if 'model' not in st.session_state:
        try:
            with st.spinner("Loading model and tokenizer... This may take a few moments."):
                st.session_state.model, st.session_state.tokenizer, st.session_state.device = model.load_model()
                st.success("Model loaded successfully!")
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            st.error("Please try refreshing the page. If the issue persists, contact support.")
            st.session_state.model = None
            st.session_state.tokenizer = None
            st.session_state.device = None
    if 'current_subject_index' not in st.session_state:
        st.session_state.current_subject_index = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'test_completed' not in st.session_state:
        st.session_state.test_completed = False
    if 'analysis_in_progress' not in st.session_state:
        st.session_state.analysis_in_progress = False
    if 'shuffled_questions' not in st.session_state:
        # Initialize shuffled questions for all subjects when starting a new test
        st.session_state.shuffled_questions = {}
        for subject in questions.get_all_subjects():
            subject_questions = questions.get_questions(subject)
            random.shuffle(subject_questions)
            st.session_state.shuffled_questions[subject] = subject_questions

def create_subject_input(subject: str) -> Dict[str, str]:
    st.markdown(f"### {subject} Questions")
    # Use the pre-shuffled questions from session state instead of getting new ones
    questions_list = st.session_state.shuffled_questions[subject]
    questions_dict = {}
    
    for i, q in enumerate(questions_list, 1):
        st.markdown(f"**Question {i}:** {q['question']}")
        col1, col2 = st.columns([3, 1])
        with col1:
            for option, text in q['options'].items():
                st.markdown(f"{option}) {text}")
        with col2:
            answer = st.selectbox(
                f"Answer",
                options=["Select an option", "a", "b", "c", "d"],
                key=f"{subject}_a{i}",
                index=0
            )
            if answer != "Select an option":
                questions_dict[f"Q{i}"] = answer
    
    return questions_dict

def calculate_subject_score(user_answers: Dict[str, str], answer_key: Dict[str, str]) -> float:
    """Calculate score for a subject based on correct answers."""
    if not user_answers:
        return 0.0
    correct = sum(1 for q, a in user_answers.items() if a == answer_key.get(q, {}).get('correct_answer'))
    return (correct / len(answer_key)) * 100

def main():
    st.title("📚 JEE Aspirant SOCA Analysis")
    
    # Get subjects in order
    subjects = questions.get_all_subjects()
    
    initialize_session_state()
    
    if not st.session_state.test_completed:
        st.markdown("""
            This dashboard helps analyze JEE aspirant responses and provides detailed SOCA analysis.
            Please answer all questions in each subject before proceeding to the next.
        """)

        current_subject = subjects[st.session_state.current_subject_index]
        
        # Show progress
        progress = (st.session_state.current_subject_index + 1) / len(subjects)
        st.progress(progress)
        st.markdown(f"**Progress:** {st.session_state.current_subject_index + 1}/{len(subjects)} subjects completed")
        
        # Create input fields for current subject
        with st.container():
            st.markdown("---")
            questions_dict = create_subject_input(current_subject)
            
            if questions_dict:
                st.session_state.user_answers[current_subject] = questions_dict
            
            # Navigation buttons
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if st.session_state.current_subject_index > 0:
                    if st.button("Previous Subject"):
                        st.session_state.current_subject_index -= 1
                        st.experimental_rerun()
            
            with col2:
                if st.session_state.current_subject_index < len(subjects) - 1:
                    if st.button("Next Subject"):
                        if current_subject in st.session_state.user_answers:
                            st.session_state.current_subject_index += 1
                            st.experimental_rerun()
                        else:
                            st.warning("Please answer at least one question before proceeding.")
                else:
                    if st.button("Submit Test"):
                        if current_subject in st.session_state.user_answers:
                            st.session_state.test_completed = True
                            st.experimental_rerun()
                        else:
                            st.warning("Please answer at least one question before submitting.")
    else:
        st.header("Analysis Results")
        
        # Check if model is loaded
        if st.session_state.model is None:
            st.error("Model failed to load. Please try refreshing the page or contact support.")
            if st.button("Take Test Again"):
                st.session_state.test_completed = False
                st.session_state.current_subject_index = 0
                st.session_state.user_answers = {}
                st.rerun()
            return
        
        # Get answer key and calculate scores
        answer_key = {}
        subject_scores = {}
        
        # Core subjects for analysis
        core_subjects = ["Physics", "Chemistry", "Mathematics"]
        
        for subject in subjects:
            # Get the questions with their full details
            questions_list = st.session_state.shuffled_questions[subject]
            answer_key[subject] = {
                f"Q{i+1}": {
                    "correct_answer": q["correct_answer"],
                    "question": q["question"]
                }
                for i, q in enumerate(questions_list)
            }
            subject_scores[subject] = calculate_subject_score(
                st.session_state.user_answers.get(subject, {}),
                answer_key[subject]
            )
        
        # Display core subject scores
        st.markdown("### 📊 Core Subject Performance")
        for subject in core_subjects:
            st.markdown(f"**{subject}:** {subject_scores[subject]:.1f}%")
        
        if not st.session_state.analysis_in_progress:
            st.session_state.analysis_in_progress = True
            try:
                # Process responses
                with st.spinner("Processing your responses... This may take a few moments."):
                    formatted_text = model.preprocess_responses(st.session_state.user_answers, answer_key)
                
                # Generate SOCA analysis
                with st.spinner("Generating comprehensive analysis... This may take a few moments."):
                    soca_analysis = model.generate_soca_analysis(
                        st.session_state.model,
                        st.session_state.tokenizer,
                        st.session_state.device,
                        formatted_text,
                        st.session_state.user_answers,
                        answer_key
                    )
                
                # Display results in a nice format
                st.markdown("### 📈 Comprehensive SOCA Analysis")
                st.markdown(soca_analysis)
                
                # Display raw responses for core subjects only
                with st.expander("View Raw Responses"):
                    st.text(formatted_text)
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.error("Please try the following:")
                st.error("1. Refresh the page and try again")
                st.error("2. Check your internet connection")
                st.error("3. If the issue persists, contact support")
            finally:
                st.session_state.analysis_in_progress = False
        
        # Add option to retake test
        if st.button("Take Test Again"):
            st.session_state.test_completed = False
            st.session_state.current_subject_index = 0
            st.session_state.user_answers = {}
            st.session_state.analysis_in_progress = False
            # Clear shuffled questions to get new order for next test
            if 'shuffled_questions' in st.session_state:
                del st.session_state.shuffled_questions
            st.rerun()

if __name__ == "__main__":
    main()