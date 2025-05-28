import json
import os

class ProgressTracker:
    def __init__(self, filepath='data/student_performance.json'):
        self.filepath = filepath
        self.data = self.load()

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=2)

    def update_score(self, user_id, topic, score):
        user_data = self.data.setdefault(user_id, {})
        topic_scores = user_data.setdefault(topic, [])
        topic_scores.append(score)
        if len(topic_scores) > 5:  # Keep last 5 scores
            topic_scores.pop(0)
        self.save()

    def get_avg_score(self, user_id, topic):
        scores = self.data.get(user_id, {}).get(topic, [])
        return sum(scores) / len(scores) if scores else 0.0
    
    def get_streak(self, user_id, topic):
        scores = self.data.get(user_id, {}).get(topic, [])
        return sum(1 for s in reversed(scores) if s >= 0.7)
    
    

