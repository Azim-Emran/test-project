from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd
import joblib

# Load data
df = pd.read_csv('/workspaces/ai_learning_assistant/model_training_pipeline/chatbot_dataset.csv')
X = df['user_input']
y = df['intent']

# Train model
model = make_pipeline(TfidfVectorizer(), LogisticRegression())
model.fit(X, y)

# Save model
joblib.dump(model, 'intent_classifier.pkl')
