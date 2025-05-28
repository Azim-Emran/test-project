from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Load your key securely

def ask_gpt(question, subject="math"):
    prompt = f"You are a helpful tutor for {subject} students. Answer this question clearly:\n\n{question}"

    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Or "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a friendly educational tutor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=300)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error contacting OpenAI: {e}"
