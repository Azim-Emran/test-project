import pandas as pd

def recommend_topic_for_student(student_id):
    df = pd.read_csv("/workspaces/ai_learning_assistant/dataset/student_performance.csv")

    # Filter for the student
    student_data = df[df['student_id'] == student_id]

    # Compute topic-level performance
    topic_scores = student_data.groupby('topic')['is_correct'].mean().reset_index()

    # Recommend topic with lowest score
    if not topic_scores.empty:
        weakest_topic = topic_scores.sort_values('is_correct').iloc[0]['topic']
        return weakest_topic
    else:
        return "Start with 'Linear Equations'"  # Fallback for new users
