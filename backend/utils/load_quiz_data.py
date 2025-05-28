import json
from pathlib import Path

def load_short_answer_quiz_data():
    # Go up from backend/utils/ to backend/ and point to quiz_dataset.json
    path = Path(__file__).resolve().parent.parent / 'quiz_dataset.json'
    with open(path, 'r', encoding='utf-8') as f:
        raw = json.load(f)

    all_questions = []

    for item in raw:
        for q in item['questions']:
            all_questions.append({
                "question": q['question'],
                "answer": q['answer'],
                "hint": q.get('hint', "Try simplifying the equation."),
                "explanation": q['explanation']
            })

    return all_questions
