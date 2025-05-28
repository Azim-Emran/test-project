from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
import joblib
import random
import json
from pathlib import Path
from models.models import db
from models.gpt_ai import ask_gpt
from models.dummy_ai import generate_response
from models.models import QuizResult
from services.adaptive_quiz_engine import get_question, get_adaptive_question, get_gpt_feedback
from services.recommendation_engine import recommend_topic_for_student
from services.progress_tracker import get_user_progress
from utils.load_quiz_data import load_short_answer_quiz_data


assistant_api_bp = Blueprint('assistant_api_bp', __name__)
ALL_QUESTIONS = load_short_answer_quiz_data()


# Load and flatten the quiz data

# Path to the directory where rl_agent.py is located
current_dir = Path(__file__).resolve().parent

# Navigate from model/ to data/quiz_data.json
data_file = current_dir.parent / 'data' / 'quiz_data.json'

# Load the JSON data
with open(data_file, 'r') as f:
    structured_data = json.load(f)


@assistant_api_bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    response = generate_response(user_input)
    return jsonify({'response': response})

# Resolve the full path to the model file
model_path = Path(__file__).resolve().parent.parent / 'model_training_pipeline' / 'intent_classifier.pkl'

# Load the model
intent_model = joblib.load(model_path)


@assistant_api_bp.route('/detect-intent', methods=['POST'])
def detect_intent():
    message = request.json.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    intent = intent_model.predict([message])[0]
    return jsonify({'intent': intent})


@assistant_api_bp.route('/recommend-topic/<int:student_id>', methods=['GET'])
def recommend_topic(student_id):
    try:
        topic = recommend_topic_for_student(student_id)
        return jsonify({'recommended_topic': topic})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@assistant_api_bp.route('/get-question/<topic>', methods=['GET'])
def get_question_for_topic(topic):
    question = get_question(topic)
    if question:
        return jsonify(question)
    else:
        return jsonify({'error': 'Topic not found'}), 404
    

@assistant_api_bp.route('/get-adaptive-question', methods=['GET'])
def get_adaptive_question():
    print("[DEBUG] Loaded", len(ALL_QUESTIONS), "questions")
    for q in ALL_QUESTIONS:
        print("[DEBUG] Sample:", q.get("question"), "|", q.get("answer"))

    if not ALL_QUESTIONS:
        return jsonify({"error": "No questions available"}), 404

    question = random.choice(ALL_QUESTIONS)
    if not question.get('question') or not question.get('answer'):
        return jsonify({"error": "Malformed question"}), 500

    return jsonify(question)



@assistant_api_bp.route('/get-progress', methods=['GET'])
def get_progress():
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401

    results = (
        QuizResult.query
        .filter_by(user_id=current_user.id)
        .all()
    )

    topic_scores = {}
    for result in results:
        if result.topic not in topic_scores:
            topic_scores[result.topic] = {"correct": 0, "total": 0}
        topic_scores[result.topic]["total"] += 1
        if result.is_correct:
            topic_scores[result.topic]["correct"] += 1

    chart_data = {
        "labels": list(topic_scores.keys()),
        "accuracies": [round((v["correct"]/v["total"])*100, 2) for v in topic_scores.values()]
    }
    return jsonify(chart_data)


@assistant_api_bp.route('/submit-answer', methods=['POST'])
@login_required
def submit_answer():
    data = request.get_json()
    topic = data.get('topic')
    is_correct = data.get('is_correct')
    time_taken = data.get('time_taken')
    attempts = data.get('attempts', 1)
    hint_used = data.get('hint_used', False)

    result = QuizResult(
        user_id=current_user.id,
        topic=topic,
        is_correct=bool(is_correct),
        time_taken=int(time_taken),
        attempts=attempts,
        hint_used=hint_used
    )
    db.session.add(result)
    db.session.commit()

    return jsonify({'message': 'Answer recorded'})

    
    
@assistant_api_bp.route('/ask-gpt', methods=['POST'])
def ask_gpt_route():
    data = request.get_json()
    question = data.get('question')
    subject = data.get('subject', 'math')

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    answer = ask_gpt(question, subject)
    return jsonify({'response': answer})



@assistant_api_bp.route('/progress/<user_id>', methods=['GET'])
def progress(user_id):
    return jsonify(get_user_progress(user_id))

@assistant_api_bp.route('/gpt-feedback', methods=['POST'])
def gpt_feedback():
    data = request.get_json()

    question = data.get('question')
    correct_answer = data.get('correct_answer')
    student_answer = data.get('student_answer')
    attempt_num = data.get('attempt_num') 

    if any(x is None for x in [question, correct_answer, student_answer, attempt_num]):
        return jsonify({"error": "Missing data"}), 400

    result = get_gpt_feedback(question, correct_answer, student_answer,attempt_num)
    return jsonify(result)
