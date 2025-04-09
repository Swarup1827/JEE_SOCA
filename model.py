import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import re

def load_model():
    try:
        # Using a smaller, more efficient model
        model_name = "google/flan-t5-base"  # Changed from large to base
        print("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        print("Loading model...")
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        # Determine the best available device
        if torch.cuda.is_available():
            device = "cuda"
            print(f"Using CUDA device: {torch.cuda.get_device_name(0)}")
        elif torch.backends.mps.is_available():
            device = "mps"
            print("Using MPS device")
        else:
            device = "cpu"
            print("Using CPU device")

        model.to(device)
        print("Model loaded successfully!")
        return model, tokenizer, device
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise

def preprocess_responses(user_answers, answer_key):
    try:
        # Define core subjects
        core_subjects = ["Physics", "Chemistry", "Mathematics"]
        
        formatted_responses = """Student Response Analysis:\n\n"""
        for subject, questions in user_answers.items():
            # Only include core subjects in raw responses
            if subject in core_subjects:
                formatted_responses += f"{subject}:\n"
                for q_no, user_ans in questions.items():
                    correct_ans = answer_key.get(subject, {}).get(q_no, {}).get("correct_answer", "Unknown")
                    status = "Correct ✅" if user_ans == correct_ans else "Incorrect ❌"
                    question_text = answer_key.get(subject, {}).get(q_no, {}).get("question", "")
                    formatted_responses += f"{q_no}. {question_text}\n   Your Answer: ({user_ans}), Correct Answer: ({correct_ans}) - {status}\n"
                formatted_responses += "\n"
        return formatted_responses
    except Exception as e:
        print(f"Error preprocessing responses: {str(e)}")
        raise

def generate_soca_analysis(model, tokenizer, device, user_text, user_answers, answer_key):
    try:
        # Calculate performance metrics for each subject
        subject_performance = {}
        for subject, questions in user_answers.items():
            correct_count = sum(1 for q_no, ans in questions.items() 
                              if ans == answer_key.get(subject, {}).get(q_no))
            total = len(questions)
            subject_performance[subject] = (correct_count / total) * 100

        # Create a more detailed prompt with performance data
        prompt = f"""
        Analyze these JEE student responses and provide a detailed SOCA analysis.
        
        Performance Summary:
        {', '.join(f'{subject}: {score:.1f}%' for subject, score in subject_performance.items())}

        Detailed Responses:
        {user_text}

        Based on the above performance, provide a detailed SOCA analysis with:
        1. Specific strengths in topics where the student performed well
        2. Clear opportunities for improvement in weaker areas
        3. Key challenges identified from incorrect answers
        4. A personalized action plan based on the performance pattern

        Format the response as:
        **Strengths:**
        - [List 3 specific strengths based on correct answers]
        
        **Opportunities:**
        - [List 2 specific opportunities based on incorrect answers]
        
        **Challenges:**
        - [List 2 specific challenges based on performance patterns]
        
        **Action Plan:**
        1. [Specific action based on weakest subject]
        2. [Specific action based on moderate performance areas]
        3. [General improvement strategy]
        """

        print("Generating personalized analysis...")
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
        
        # Optimized generation parameters
        outputs = model.generate(
            input_ids=inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=512,
            min_length=200,
            num_beams=3,
            temperature=0.8,  # Slightly increased for more variation
            top_k=40,
            top_p=0.95,
            repetition_penalty=1.3,  # Increased to reduce repetition
            no_repeat_ngram_size=3,  # Increased to reduce repetition
            early_stopping=True,
            do_sample=True
        )

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        
        if not generated_text or len(generated_text) < 100:
            print("Generated text too short, falling back to detailed analysis")
            return generate_fallback_soca(user_answers, answer_key)

        # Enhanced section parsing
        sections = {}
        section_patterns = {
            "Strengths": r"(?i)\*\*Strengths:\*\*[\s\n]*(.*?)(?=\n\s*\*\*|$)",
            "Opportunities": r"(?i)\*\*Opportunities:\*\*[\s\n]*(.*?)(?=\n\s*\*\*|$)",
            "Challenges": r"(?i)\*\*Challenges:\*\*[\s\n]*(.*?)(?=\n\s*\*\*|$)",
            "Action Plan": r"(?i)\*\*Action Plan:\*\*[\s\n]*(.*?)(?=\n\s*\*\*|$)"
        }

        for section, pattern in section_patterns.items():
            match = re.search(pattern, generated_text, re.DOTALL)
            if match:
                content = match.group(1).strip()
                content = re.sub(r'^\s*[-*]\s*', '- ', content, flags=re.MULTILINE)
                content = re.sub(r'^\s*\d+\.\s*', '1. ', content, flags=re.MULTILINE)
                sections[section] = content
            else:
                print(f"Warning: Could not find {section} section")
                return generate_fallback_soca(user_answers, answer_key)

        # Format the final output with performance summary
        formatted_output = "**Performance Summary:**\n"
        for subject, score in subject_performance.items():
            formatted_output += f"- {subject}: {score:.1f}%\n"
        formatted_output += "\n"

        for section in ["Strengths", "Opportunities", "Challenges", "Action Plan"]:
            if section in sections and sections[section]:
                formatted_output += f"**{section}:**\n{sections[section]}\n\n"

        print("Personalized analysis generated successfully!")
        return formatted_output

    except Exception as e:
        print(f"Error in generate_soca_analysis: {str(e)}")
        return generate_fallback_soca(user_answers, answer_key)

def generate_fallback_soca(user_answers, answer_key):
    # Enhanced topic mapping for more specific analysis
    topic_mapping = {
        "Physics": {
            "Mechanics": [
                "circular motion", "kinetic energy", "acceleration", "velocity", "force", "motion",
                "momentum", "work", "power", "energy", "rotational", "newton", "gravity", "friction"
            ],
            "Electromagnetism": [
                "electric current", "potential difference", "charge", "ampere", "volt",
                "magnetic field", "electromagnetic", "capacitor", "inductor", "resistance",
                "ohm", "conductor", "insulator", "electric field"
            ],
            "Waves & Oscillations": [
                "pendulum", "light", "refraction", "wave", "oscillation", "frequency",
                "amplitude", "wavelength", "sound", "interference", "diffraction", "polarization",
                "standing wave", "resonance"
            ],
            "Thermodynamics": [
                "specific heat", "gas", "temperature", "heat", "thermal",
                "entropy", "pressure", "volume", "adiabatic", "isothermal",
                "carnot cycle", "heat engine", "thermodynamic"
            ],
            "Modern Physics": [
                "quantum", "photoelectric", "nuclear", "relativity", "atom",
                "particle", "wave-particle", "radiation", "half-life", "fusion",
                "fission", "quantum mechanics"
            ],
            "Optics": [
                "lens", "mirror", "reflection", "refraction", "prism",
                "optical", "focal length", "magnification", "telescope", "microscope",
                "ray diagram", "total internal reflection"
            ]
        },
        "Chemistry": {
            "Physical Chemistry": [
                "pH", "solution", "gas", "pressure", "temperature", "equilibrium",
                "kinetics", "thermochemistry", "electrochemistry", "surface chemistry",
                "colligative", "phase rule", "conductivity", "electrolysis"
            ],
            "Inorganic Chemistry": [
                "noble gas", "atomic number", "electron", "periodic", "atomic",
                "transition metal", "coordination compound", "crystal", "ionic",
                "metallurgy", "acid base", "salt", "oxidation state", "chemical bonding"
            ],
            "Organic Chemistry": [
                "glucose", "molecular formula", "compound", "carbon", "alkane",
                "alkene", "alkyne", "alcohol", "ether", "aldehyde", "ketone",
                "carboxylic acid", "amine", "benzene", "aromatic", "polymer",
                "isomerism", "stereochemistry"
            ],
            "Chemical Reactions": [
                "redox", "acid", "base", "reaction", "strong acid", "strong base",
                "neutralization", "precipitation", "decomposition", "combination",
                "displacement", "double displacement", "catalysis"
            ],
            "Analytical Chemistry": [
                "titration", "indicator", "qualitative", "quantitative", "analysis",
                "chromatography", "spectroscopy", "gravimetric", "volumetric"
            ]
        },
        "Mathematics": {
            "Calculus": [
                "derivative", "integration", "limit", "function", "differential",
                "maxima", "minima", "continuity", "differentiability", "application",
                "partial derivative", "definite integral", "indefinite integral"
            ],
            "Algebra": [
                "equation", "matrix", "determinant", "solution", "polynomial",
                "quadratic", "cubic", "complex number", "vector", "progression",
                "sequence", "series", "permutation", "combination"
            ],
            "Trigonometry": [
                "sin", "cos", "tan", "angle", "theta", "inverse trigonometric",
                "trigonometric equation", "height and distance", "triangle",
                "periodic function", "identities", "transformation"
            ],
            "Coordinate Geometry": [
                "circle", "line", "point", "radius", "center", "parabola",
                "ellipse", "hyperbola", "conic section", "distance formula",
                "section formula", "parametric form", "3D geometry"
            ],
            "Vectors & 3D": [
                "vector", "scalar", "dot product", "cross product", "direction cosine",
                "plane", "straight line", "skew lines", "shortest distance",
                "angle between lines", "angle between planes"
            ],
            "Statistics & Probability": [
                "probability", "mean", "median", "mode", "standard deviation",
                "variance", "random variable", "binomial", "normal distribution",
                "correlation", "regression", "sampling"
            ]
        }
    }

    # Calculate detailed performance metrics
    subject_performance = {}
    topic_performance = {}
    question_analysis = {}
    
    for subject, questions in user_answers.items():
        if subject in ["Well-being Assessment", "Time Management"]:
            continue  # Skip non-core subjects
            
        correct_count = 0
        topic_correct = {topic: 0 for topic in topic_mapping.get(subject, {})}
        topic_total = {topic: 0 for topic in topic_mapping.get(subject, {})}
        question_analysis[subject] = []
        
        for q_no, user_ans in questions.items():
            correct_ans = answer_key.get(subject, {}).get(q_no, {}).get("correct_answer", "Unknown")
            question_text = answer_key.get(subject, {}).get(q_no, {}).get("question", "").lower()
            is_correct = user_ans == correct_ans
            
            if is_correct:
                correct_count += 1
            
            # Store question analysis
            question_analysis[subject].append({
                "question": question_text,
                "is_correct": is_correct,
                "topics": []
            })
            
            # Map question to topics based on keywords
            if subject in topic_mapping:
                for topic, keywords in topic_mapping[subject].items():
                    if any(keyword.lower() in question_text for keyword in keywords):
                        topic_total[topic] += 1
                        question_analysis[subject][-1]["topics"].append(topic)
                        if is_correct:
                            topic_correct[topic] += 1
        
        total_questions = len(questions)
        if total_questions > 0:
            subject_performance[subject] = (correct_count / total_questions) * 100
            
            for topic in topic_correct:
                if topic_total[topic] > 0:
                    if subject not in topic_performance:
                        topic_performance[subject] = {}
                    topic_performance[subject][topic] = (topic_correct[topic] / topic_total[topic]) * 100

    # Generate detailed analysis
    strengths = []
    opportunities = []
    challenges = []
    action_items = []
    detailed_recommendations = []

    # Analyze strengths with specific topics
    for subject, performance in subject_performance.items():
        if performance >= 70:
            strengths.append(f"Strong overall performance in {subject} ({performance:.1f}%)")
            
        if subject in topic_performance:
            strong_topics = [(topic, score) for topic, score in topic_performance[subject].items() if score >= 70]
            if strong_topics:
                for topic, score in strong_topics:
                    strengths.append(f"Excellent understanding of {topic} in {subject} ({score:.1f}%)")
                    # Add specific recommendations for maintaining strength
                    detailed_recommendations.append(f"To maintain strength in {topic} ({subject}):")
                    detailed_recommendations.append(f"- Practice advanced problems in {topic}")
                    detailed_recommendations.append(f"- Help peers understand {topic} concepts")
                    detailed_recommendations.append(f"- Explore real-world applications of {topic}")

    # Analyze opportunities and challenges with specific recommendations
    for subject, performance in subject_performance.items():
        if subject in topic_performance:
            weak_topics = [(topic, score) for topic, score in topic_performance[subject].items() if score < 50]
            moderate_topics = [(topic, score) for topic, score in topic_performance[subject].items() if 50 <= score < 70]
            
            for topic, score in weak_topics:
                challenges.append(f"Needs significant improvement in {topic} ({subject}) - {score:.1f}%")
                opportunities.append(f"Focus on strengthening {topic} in {subject}")
                # Add specific recommendations for improvement
                detailed_recommendations.append(f"To improve in {topic} ({subject}):")
                detailed_recommendations.append(f"- Review fundamental concepts of {topic}")
                detailed_recommendations.append(f"- Solve basic to medium level problems in {topic}")
                detailed_recommendations.append(f"- Watch video lectures on {topic}")
                detailed_recommendations.append(f"- Create concept maps for {topic}")
            
            for topic, score in moderate_topics:
                opportunities.append(f"Potential to excel in {topic} ({subject}) - Current: {score:.1f}%")
                detailed_recommendations.append(f"To excel in {topic} ({subject}):")
                detailed_recommendations.append(f"- Practice more complex problems in {topic}")
                detailed_recommendations.append(f"- Focus on connecting {topic} with other topics")
                detailed_recommendations.append(f"- Take timed tests focusing on {topic}")

    # Generate comprehensive action plan
    if subject_performance:
        weakest_subject = min(subject_performance.items(), key=lambda x: x[1])[0]
        weakest_topics = []
        for subject, topics in topic_performance.items():
            weak = [(topic, score) for topic, score in topics.items() if score < 50]
            weakest_topics.extend([(subject, topic, score) for topic, score in weak])
        
        action_items.extend([
            f"1. Create focused study plan for {weakest_subject} with emphasis on weak topics",
            "2. Daily Practice Schedule:",
            f"   - Morning: Focus on {weakest_subject} concepts",
            "   - Afternoon: Problem-solving practice",
            "   - Evening: Review and revision",
            "3. Weekly Assessment Plan:",
            "   - Take topic-wise tests",
            "   - Analyze mistakes and patterns",
            "   - Update study strategy based on results",
            "4. Resource Utilization:",
            "   - Use video lectures for difficult concepts",
            "   - Join study groups for collaborative learning",
            "   - Consult reference books for detailed understanding",
            "5. Progress Tracking:",
            "   - Maintain a progress journal",
            "   - Track improvement in weak areas",
            "   - Set weekly and monthly goals"
        ])
    
    # Format the analysis with more detail
    analysis = f"""
**Performance Summary:**
{chr(10).join(f'- {subject}: {score:.1f}%' for subject, score in subject_performance.items())}

**Detailed Strengths Analysis:**
{chr(10).join(f'- {s}' for s in strengths) if strengths else '- Keep working on improving your performance'}

**Key Opportunities for Improvement:**
{chr(10).join(f'- {o}' for o in opportunities) if opportunities else '- Focus on fundamental concepts'}

**Critical Challenges to Address:**
{chr(10).join(f'- {c}' for c in challenges) if challenges else '- Maintain consistent practice'}

**Detailed Recommendations:**
{chr(10).join(detailed_recommendations)}

**Comprehensive Action Plan:**
{chr(10).join(action_items)}

**Additional Notes:**
- Focus on understanding the underlying concepts rather than memorizing solutions
- Practice time management during problem-solving
- Regularly review and revise previously learned concepts
- Maintain a healthy balance between study and rest
- Track your progress and adjust your study plan accordingly
"""
    return analysis

if __name__ == "__main__":
    try:
        model, tokenizer, device = load_model()

        # Test data
        user_answers = {
            "Physics": {"Q1": "d", "Q2": "c", "Q3": "b"},
            "Mathematics": {"Q21": "c", "Q22": "a"},
            "Problem-Solving": {"Q31": "b", "Q32": "d"}
        }

        answer_key = {
            "Physics": {"Q1": "d", "Q2": "c", "Q3": "b"},
            "Mathematics": {"Q21": "c", "Q22": "a"},
            "Problem-Solving": {"Q31": "b", "Q32": "d"}
        }

        formatted_text = preprocess_responses(user_answers, answer_key)
        soca_analysis = generate_soca_analysis(model, tokenizer, device, formatted_text, user_answers, answer_key)
        print("\nGenerated SOCA Analysis:\n")
        print(soca_analysis)
    except Exception as e:
        print(f"Error in main execution: {str(e)}")