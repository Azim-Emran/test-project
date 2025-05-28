import json
import os

def load_all_questions_data():
    path = os.path.join('dataset', 'quiz_dataset.json')
    with open(path, 'r', encoding='utf-8') as f:
        raw = json.load(f)

    all_questions = []

    for item in raw:
        topic = item.get('topic')
        for q in item['questions']:
            all_questions.append({
                "question_text": q['question'],
                "answer": q['answer'],
                "hint": q.get('hint', "Try simplifying the equation."),
                "explanation": q.get('explanation', ""),
                "topic": topic  # ✅ Add this
            })

    return all_questions
