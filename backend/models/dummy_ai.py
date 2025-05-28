from services.adaptive_quiz_engine import get_question

def generate_response(user_input):
    # Dummy logic. Replace with ML model/API integration.
    return f"AI Assistant response to: {user_input}"


# Content Recommender (Rule-based or ML)
# Replace this with collaborative filtering or reinforcement learning using more data.
def recommend_next_topic(student_history, topic_accuracy):
    # Very basic rule: Recommend topic with lowest accuracy
    return sorted(topic_accuracy.items(), key=lambda x: x[1])[0][0]


# Quiz Engine Logic (Adaptive)
def select_next_question(topic, performance_level):
    if performance_level == "low":
        return get_question(topic, difficulty="easy")
    elif performance_level == "high":
        return get_question(topic, difficulty="hard")
