from flask_login import current_user
import random
import json
from models.models import QuizResult
import openai

from models.gpt_ai import ask_gpt

def get_gpt_feedback(question, correct_answer, student_answer, attempt_num):
    if attempt_num < 3:
        prompt = f"""
    You are evaluating a student's short written math answer.
    Make sure the hint and explanation provided can be understandable by secondary students.

    QUESTION: {question}
    CORRECT ANSWER: {correct_answer}
    STUDENT'S ANSWER: {student_answer}

    Determine:
    1. Is the student's answer correct? (Only output true or false)
    2. If correct, explain briefly why it's correct.
    3. If incorrect, give a helpful hint without revealing the full solution. Do not give the actual answer.
    No need to include whether the student is correct or wrong in the hint. Use <br> when you are putting the text in new lines.

    Return the result in this exact JSON format:
    {{
    "is_correct": true or false,
    "explanation": "...",
    "hint": "..."
    }}
    """
    else:
        prompt = f"""
    You are evaluating a student's short written math answer.
    Make sure the hint and explanation provided can be understandable by secondary students.

    QUESTION: {question}
    CORRECT ANSWER: {correct_answer}
    STUDENT'S ANSWER: {student_answer}

    Determine:
    1. Is the student's answer correct? (Only output true or false).
    2. If correct, explain briefly why it's correct.
    3. If incorrect, explain clearly what the student did wrong AND give a step-by-step explanation on how to solve the problem (with step-by-step working). Add this to "explanation".
    In your explanation, you should say "you" which refers to the "student" as if you are talking to the student themselves.
    No need to include whether the student is correct or wrong in the explanation. Use <br> when you are putting the text in new lines.


    Return the result in this exact JSON format:
    {{
    "is_correct": true or false,
    "explanation": "...",
    "hint": "" 
    }}

    """


    response = ask_gpt(prompt)

    # Try parsing the GPT response into JSON
    import json
    try:
        return json.loads(response)
    except Exception as e:
        # Fallback if GPT responds in natural language
        return {
            "is_correct": False,
            "explanation": "⚠️ Unable to parse GPT response. Please try again.",
            "hint": "Check your formatting or contact support."
        }


def load_quiz_data():
    with open('/workspaces/ai_learning_assistant/model_training_pipeline/quiz_dataset.json') as f:
        return json.load(f)

def get_question(topic, performance_level='medium'):
    data = load_quiz_data()
    topic_data = next((t for t in data if t["concept"] == topic), None)

    if topic_data:
        questions = topic_data['questions']
        # Simulate difficulty: pick random for now
        return random.choice(questions)
    return None

def get_performance_level(topic):
    results = QuizResult.query.filter_by(user_id=current_user.id, topic=topic).all()
    if not results:
        return 'easy'
    
    correct_ratio = sum(r.is_correct for r in results) / len(results)
    if correct_ratio >= 0.8:
        return 'hard'
    elif correct_ratio >= 0.5:
        return 'medium'
    return 'easy'

def get_adaptive_question(topic):
    quiz_data = load_quiz_data()
    topic_data = next((t for t in quiz_data if t['concept'] == topic), None)

    if not topic_data:
        return None

    performance_level = get_performance_level(topic)
    filtered = [q for q in topic_data['questions'] if q['difficulty'] == performance_level]

    if filtered:
        return random.choice(filtered)
    else:
        return random.choice(topic_data['questions'])  # Fallback
