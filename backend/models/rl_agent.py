from pathlib import Path
import random
import json
import os

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.actions = actions
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate

    def get_state_key(self, state):
        return str(state)

    def choose_action(self, state):
        state_key = self.get_state_key(state)
        if random.uniform(0, 1) < self.epsilon or state_key not in self.q_table:
            return random.choice(self.actions)
        return max(self.q_table[state_key], key=self.q_table[state_key].get)

    def learn(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0.0 for a in self.actions}
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {a: 0.0 for a in self.actions}

        predict = self.q_table[state_key][action]
        target = reward + self.gamma * max(self.q_table[next_state_key].values())

        self.q_table[state_key][action] = predict + self.alpha * (target - predict)

    def save_q_table(self, file_path='data/q_table.json'):
        with open(file_path, 'w') as f:
            json.dump(self.q_table, f)

    def load_q_table(self, file_path='data/q_table.json'):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self.q_table = json.load(f)


# Load and flatten the quiz data

# Path to the directory where rl_agent.py is located
current_dir = Path(__file__).resolve().parent

# Navigate from model/ to data/quiz_data.json
data_file = current_dir.parent / 'data' / 'quiz_data.json'

# Load the JSON data
with open(data_file, 'r') as f:
    structured_data = json.load(f)

ALL_QUESTIONS = []
for topic in structured_data:
    for q in topic['questions']:
        ALL_QUESTIONS.append(q)