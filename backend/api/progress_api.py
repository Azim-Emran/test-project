from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models.progress_tracker import ProgressTracker

progress_api = Blueprint('progress_api', __name__)
tracker = ProgressTracker()

@progress_api.route('/api/get-progress', methods=['GET'])
@login_required
def get_progress():
    user_id = current_user.id  # comes from Flask-Login
    data = tracker.data.get(user_id, {})
    labels = list(data.keys())
    accuracies = [
        round(sum(scores)/len(scores) * 100, 2) if scores else 0 
        for scores in data.values()
    ]

    return jsonify({
        "labels": labels,
        "accuracies": accuracies
    })
