from typing import Dict, List, Any
import random

# Define the order of subjects
SUBJECT_ORDER = ["Physics", "Chemistry", "Mathematics", "Well-being Assessment", "Time Management"]

# Sample questions for each subject
QUESTIONS = {
    "Physics": [
        {
            "question": "A particle moves in a circular path of radius r with uniform speed v. The magnitude of its acceleration is:",
            "options": {
                "a": "v/r",
                "b": "v²/r",
                "c": "v/r²",
                "d": "v²/r²"
            },
            "correct_answer": "b"
        },
        {
            "question": "The SI unit of electric current is:",
            "options": {
                "a": "Volt",
                "b": "Watt",
                "c": "Ampere",
                "d": "Ohm"
            },
            "correct_answer": "c"
        },
        {
            "question": "A body of mass 2 kg is moving with a velocity of 3 m/s. Its kinetic energy is:",
            "options": {
                "a": "6 J",
                "b": "9 J",
                "c": "12 J",
                "d": "18 J"
            },
            "correct_answer": "b"
        },
        {
            "question": "The refractive index of a medium is 1.5. The speed of light in this medium is:",
            "options": {
                "a": "2 × 10⁸ m/s",
                "b": "1.5 × 10⁸ m/s",
                "c": "1 × 10⁸ m/s",
                "d": "0.5 × 10⁸ m/s"
            },
            "correct_answer": "a"
        },
        {
            "question": "A spring of force constant k is cut into two equal parts. The force constant of each part is:",
            "options": {
                "a": "k/2",
                "b": "k",
                "c": "2k",
                "d": "4k"
            },
            "correct_answer": "c"
        },
        {
            "question": "The work done in moving a charge of 2C through a potential difference of 5V is:",
            "options": {
                "a": "2.5 J",
                "b": "5 J",
                "c": "10 J",
                "d": "20 J"
            },
            "correct_answer": "c"
        },
        {
            "question": "The time period of a simple pendulum depends on:",
            "options": {
                "a": "Mass of the bob",
                "b": "Length of the string",
                "c": "Amplitude of oscillation",
                "d": "All of these"
            },
            "correct_answer": "b"
        },
        {
            "question": "A body is moving with uniform acceleration. Its velocity after 5 seconds is 25 m/s and after 8 seconds is 34 m/s. The acceleration is:",
            "options": {
                "a": "2 m/s²",
                "b": "3 m/s²",
                "c": "4 m/s²",
                "d": "5 m/s²"
            },
            "correct_answer": "b"
        },
        {
            "question": "The ratio of specific heats (γ) for a monatomic gas is:",
            "options": {
                "a": "1.33",
                "b": "1.40",
                "c": "1.67",
                "d": "1.80"
            },
            "correct_answer": "c"
        },
        {
            "question": "A ray of light is incident at an angle of 45° on a glass slab. The refractive index of glass is 1.5. The angle of refraction is:",
            "options": {
                "a": "30°",
                "b": "45°",
                "c": "60°",
                "d": "90°"
            },
            "correct_answer": "a"
        }
    ],
    "Chemistry": [
        {
            "question": "Which of the following is a noble gas?",
            "options": {
                "a": "Nitrogen",
                "b": "Helium",
                "c": "Chlorine",
                "d": "Oxygen"
            },
            "correct_answer": "b"
        },
        {
            "question": "The atomic number of Carbon is:",
            "options": {
                "a": "4",
                "b": "6",
                "c": "8",
                "d": "10"
            },
            "correct_answer": "b"
        },
        {
            "question": "Which of the following is a strong acid?",
            "options": {
                "a": "Acetic acid",
                "b": "Hydrochloric acid",
                "c": "Carbonic acid",
                "d": "Citric acid"
            },
            "correct_answer": "b"
        },
        {
            "question": "The molecular formula of glucose is:",
            "options": {
                "a": "C₆H₁₂O₅",
                "b": "C₆H₁₂O₆",
                "c": "C₅H₁₀O₅",
                "d": "C₅H₁₀O₆"
            },
            "correct_answer": "b"
        },
        {
            "question": "Which of the following is an example of a redox reaction?",
            "options": {
                "a": "NaCl + AgNO₃ → AgCl + NaNO₃",
                "b": "2H₂ + O₂ → 2H₂O",
                "c": "HCl + NaOH → NaCl + H₂O",
                "d": "CaCO₃ → CaO + CO₂"
            },
            "correct_answer": "b"
        },
        {
            "question": "The pH of a neutral solution at 25°C is:",
            "options": {
                "a": "0",
                "b": "7",
                "c": "14",
                "d": "1"
            },
            "correct_answer": "b"
        },
        {
            "question": "Which of the following is a greenhouse gas?",
            "options": {
                "a": "N₂",
                "b": "O₂",
                "c": "CO₂",
                "d": "H₂"
            },
            "correct_answer": "c"
        },
        {
            "question": "The process of conversion of solid directly to gas is called:",
            "options": {
                "a": "Sublimation",
                "b": "Evaporation",
                "c": "Condensation",
                "d": "Melting"
            },
            "correct_answer": "a"
        },
        {
            "question": "Which of the following is a strong base?",
            "options": {
                "a": "NH₃",
                "b": "NaOH",
                "c": "CH₃COOH",
                "d": "H₂O"
            },
            "correct_answer": "b"
        },
        {
            "question": "The number of electrons in the outermost shell of an atom is called:",
            "options": {
                "a": "Atomic number",
                "b": "Mass number",
                "c": "Valency",
                "d": "Atomic mass"
            },
            "correct_answer": "c"
        }
    ],
    "Mathematics": [
        {
            "question": "If sin θ + cos θ = 1, then the value of sin θ cos θ is:",
            "options": {
                "a": "0",
                "b": "1/2",
                "c": "1",
                "d": "2"
            },
            "correct_answer": "a"
        },
        {
            "question": "The derivative of x² with respect to x is:",
            "options": {
                "a": "x",
                "b": "2x",
                "c": "x²",
                "d": "2x²"
            },
            "correct_answer": "b"
        },
        {
            "question": "The value of ∫(2x + 3)dx from 0 to 2 is:",
            "options": {
                "a": "4",
                "b": "6",
                "c": "8",
                "d": "10"
            },
            "correct_answer": "d"
        },
        {
            "question": "If A is a 2×2 matrix with determinant 3, then det(2A) is:",
            "options": {
                "a": "3",
                "b": "6",
                "c": "9",
                "d": "12"
            },
            "correct_answer": "d"
        },
        {
            "question": "The number of terms in the expansion of (a + b)⁴ is:",
            "options": {
                "a": "3",
                "b": "4",
                "c": "5",
                "d": "6"
            },
            "correct_answer": "c"
        },
        {
            "question": "The equation of the circle with center (2,3) and radius 4 is:",
            "options": {
                "a": "(x-2)² + (y-3)² = 4",
                "b": "(x-2)² + (y-3)² = 16",
                "c": "(x+2)² + (y+3)² = 4",
                "d": "(x+2)² + (y+3)² = 16"
            },
            "correct_answer": "b"
        },
        {
            "question": "The probability of getting a head when tossing a fair coin is:",
            "options": {
                "a": "0.25",
                "b": "0.5",
                "c": "0.75",
                "d": "1"
            },
            "correct_answer": "b"
        },
        {
            "question": "The value of lim(x→0) sin(x)/x is:",
            "options": {
                "a": "0",
                "b": "1",
                "c": "∞",
                "d": "Does not exist"
            },
            "correct_answer": "b"
        },
        {
            "question": "The number of ways to arrange 5 different books on a shelf is:",
            "options": {
                "a": "5",
                "b": "25",
                "c": "120",
                "d": "625"
            },
            "correct_answer": "c"
        },
        {
            "question": "The solution of the equation 2x + 3 = 7 is:",
            "options": {
                "a": "x = 1",
                "b": "x = 2",
                "c": "x = 3",
                "d": "x = 4"
            },
            "correct_answer": "b"
        }
    ],
    "Well-being Assessment": [
        {
            "question": "How would you rate your current stress level?",
            "options": {
                "a": "Very High",
                "b": "High",
                "c": "Moderate",
                "d": "Low"
            },
            "correct_answer": "d"
        },
        {
            "question": "How many hours of sleep do you get on average?",
            "options": {
                "a": "Less than 4 hours",
                "b": "4-6 hours",
                "c": "6-8 hours",
                "d": "More than 8 hours"
            },
            "correct_answer": "c"
        },
        {
            "question": "How often do you exercise?",
            "options": {
                "a": "Never",
                "b": "1-2 times per week",
                "c": "3-4 times per week",
                "d": "Daily"
            },
            "correct_answer": "d"
        },
        {
            "question": "How do you typically handle academic pressure?",
            "options": {
                "a": "Avoid thinking about it",
                "b": "Get anxious and stressed",
                "c": "Talk to friends/family",
                "d": "Use structured coping strategies"
            },
            "correct_answer": "d"
        },
        {
            "question": "How confident are you in your ability to achieve your JEE goals?",
            "options": {
                "a": "Not confident at all",
                "b": "Slightly confident",
                "c": "Moderately confident",
                "d": "Very confident"
            },
            "correct_answer": "d"
        }
    ],
    "Time Management": [
        {
            "question": "How do you typically plan your study schedule?",
            "options": {
                "a": "No planning",
                "b": "Basic daily list",
                "c": "Weekly schedule",
                "d": "Detailed monthly planner"
            },
            "correct_answer": "d"
        },
        {
            "question": "How do you handle study breaks?",
            "options": {
                "a": "No breaks",
                "b": "Random breaks",
                "c": "Fixed time breaks",
                "d": "Pomodoro technique"
            },
            "correct_answer": "d"
        },
        {
            "question": "How do you prioritize your study topics?",
            "options": {
                "a": "No prioritization",
                "b": "Based on difficulty",
                "c": "Based on exam weightage",
                "d": "Based on both difficulty and weightage"
            },
            "correct_answer": "d"
        },
        {
            "question": "How do you handle unexpected disruptions in your study schedule?",
            "options": {
                "a": "Get frustrated and give up",
                "b": "Skip the disrupted topic",
                "c": "Try to make up time later",
                "d": "Have a flexible backup plan"
            },
            "correct_answer": "d"
        },
        {
            "question": "How do you review and adjust your study plan?",
            "options": {
                "a": "Never review",
                "b": "Only when problems occur",
                "c": "Weekly review",
                "d": "Daily review and adjustment"
            },
            "correct_answer": "d"
        }
    ]
}

def get_questions(subject: str) -> List[Dict[str, Any]]:
    """
    Retrieve questions for a specific subject in random order.
    
    Args:
        subject (str): The subject name
        
    Returns:
        List[Dict[str, Any]]: List of questions with their options and correct answers in random order
    """
    questions = QUESTIONS.get(subject, [])
    # Create a copy of the questions list to avoid modifying the original
    shuffled_questions = questions.copy()
    # Shuffle the questions randomly
    random.shuffle(shuffled_questions)
    return shuffled_questions

def get_all_subjects() -> List[str]:
    """
    Get a list of all available subjects in the specified order.
    
    Returns:
        List[str]: List of subject names in the order: Physics, Chemistry, Mathematics, Well-being, Time Management
    """
    return SUBJECT_ORDER

def get_question_count(subject: str) -> int:
    """
    Get the number of questions available for a subject.
    
    Args:
        subject (str): The subject name
        
    Returns:
        int: Number of questions available
    """
    return len(QUESTIONS.get(subject, [])) 