import pandas as pd
import random

topics = ["Linear Equations", "Angles", "Fractions"]
data = []

for student_id in range(1, 6):
    for topic in topics:
        for i in range(3):  # 3 questions per topic
            question_id = f"{topic[:2]}Q{i}"
            is_correct = random.choice([1, 0])
            time_taken = random.randint(10, 60)
            data.append([student_id, topic, question_id, is_correct, time_taken])

df_perf = pd.DataFrame(data, columns=["student_id", "topic", "question_id", "is_correct", "time_taken"])
df_perf.to_csv("student_performance.csv", index=False)
