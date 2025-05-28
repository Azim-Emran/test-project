import json
import pandas as pd

# For Umy
with open(r'C:\Users\User\ai_learning_assistant\dataset\math_questions_dataset.json') as f:
    data = json.load(f)


# For Azem
# with open(r'C:\Users\ASUS\Documents\Reka Lab\MVP2\web\ai_learning_assistant\dataset\math_questions_dataset.json') as f:
#    data = json.load(f)

df = pd.json_normalize(data)

df = df[['question_id', 'question_text', 'answer', 'difficulty', 'topic', 'sub_topic', 'concept',
         'hint1', 'hint2', 'detailed_solution', 'grade_level']]

# Save to cleaned dataset
df.to_json('cleaned_quiz_dataset.json', orient='records', indent=2)
print("✅ Cleaned and saved dataset.")