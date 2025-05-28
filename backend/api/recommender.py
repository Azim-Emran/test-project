# backend/recommender.py
import json
import os
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DATA_PATH = r"C:\Users\User\ai_learning_assistant\data\user_progress.json"

def generate_explanation(user_id, topic):
    # Load performance data
    user_data = load_user_data(user_id)

    history = ", ".join([f"{t}: {s}%" for t, s in user_data.items()])
    prompt = f"""
    You are a helpful educational assistant. A student has completed quizzes on various topics. 
    Based on their performance history, explain briefly why you are recommending the topic: {topic}.
    Student history: {history}
    Give a short motivational reason.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a friendly learning assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )

    explanation = response['choices'][0]['message']['content'].strip()
    return explanation

def load_user_data(user_id):
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data.get(str(user_id), {})

def recommend_topic(user_id):
    user_data = load_user_data(user_id)

    # Define topics and sort by lowest performance
    all_topics = ["Linear Equations", "Quadratic Equations", "Angles", "Geometry", "Algebra", "Graphing"]
    scores = {topic: user_data.get(topic, 0) for topic in all_topics}

    # Recommend the topic with the lowest score
    recommended = min(scores, key=scores.get)
    return recommended
