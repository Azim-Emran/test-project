chat_data = [
    {"user_input": "Can you explain how to solve equations?", "intent": "ask_explanation", "response": "Sure. Let's go over solving linear equations."},
    {"user_input": "Give me a quiz on angles", "intent": "request_quiz", "response": "Starting a quiz on angles."},
    {"user_input": "I’m confused about this topic", "intent": "express_confusion", "response": "Would you like a hint or an example?"}
]

import pandas as pd
df_chat = pd.DataFrame(chat_data)
df_chat.to_csv("chatbot_dataset.csv", index=False)
