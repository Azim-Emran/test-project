from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import pandas as pd

# Load and prepare dataset
data = pd.read_json('/workspaces/ai_learning_assistant/dataset/chatbot_dataset.json')
X, y = data['user_input'], data['intent']

# Build and train
model = make_pipeline(TfidfVectorizer(), LogisticRegression())
model.fit(X, y)

# Save model
import joblib
joblib.dump(model, 'intent_classifier.pkl')
