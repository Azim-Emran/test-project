from flask import Blueprint, request, jsonify
from models.rl_agent import QLearningAgent
import json
import os

recommend_bp = Blueprint('recommend', __name__)

# Define possible actions (topics/difficulties)
ACTIONS = ["Algebra Easy", "Algebra Medium", "Geometry Easy", "Geometry Medium"]
agent = QLearningAgent(actions=ACTIONS)
agent.load_q_table(os.path.join("data", "q_table.json"))

@recommend_bp.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    state = data.get('state')  # E.g. {"grade": 9, "score_avg": 0.65}
    action = agent.choose_action(state)
    return jsonify({"recommended": action})

@recommend_bp.route('/reward', methods=['POST'])
def reward():
    data = request.json
    state = data['state']
    action = data['action']
    reward = data['reward']
    next_state = data['next_state']

    agent.learn(state, action, reward, next_state)
    agent.save_q_table(os.path.join("data", "q_table.json"))
    return jsonify({"status": "Q-table updated"})
