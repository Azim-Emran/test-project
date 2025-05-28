# auth/quiz_routes.py

from flask import Blueprint, request, jsonify
from models.progress_tracker import ProgressTracker
import requests

progress_tracker = ProgressTracker()

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    data = request.json
    user_id = data['user_id']
    answers = data['answers']
    topic = data['topic']
    difficulty = data['difficulty']
    correct_count = sum(1 for a in answers if a['correct'])

    score = correct_count / len(answers)
    prev_avg = progress_tracker.get_avg_score(user_id, topic)
    reward = 1 if score >= 0.7 else -1  # basic rule: pass/fail
    state = {"grade": data.get("grade", 9), "score_avg": data.get("previous_avg", 0.5)}
    action = f"{topic} {difficulty}"
    next_state = {"grade": data.get("grade", 9), "score_avg": score}
    
    
    # Update history
    progress_tracker.update_score(user_id, topic, score)

    # Reward calculation logic
    reward = 0
    if score > prev_avg:
        reward = 1  # Improvement
    elif score == prev_avg:
        reward = 0.2  # Maintained performance
    else:
        reward = -1  # Regression

    state = {"grade": data.get("grade", 9), "score_avg": round(prev_avg, 2)}
    action = f"{topic} {difficulty}"
    next_state = {"grade": data.get("grade", 9), "score_avg": round(score, 2)}

    try:
        requests.post('http://localhost:5000/api/reward', json={
            "state": state,
            "action": action,
            "reward": reward,
            "next_state": next_state
        })
    except Exception as e:
        print("Error sending reward:", e)

    return jsonify({
        "message": "Quiz submitted",
        "score": score,
        "reward": reward,
        "previous_avg": prev_avg
    })