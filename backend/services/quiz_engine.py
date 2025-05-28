import random

def generate_quiz(user_profile, performance_score):
    if performance_score < 40:
        level = 'easy'
    elif performance_score < 70:
        level = 'medium'
    else:
        level = 'hard'
    
    # Dummy questions, ideally pull from DB
    questions = {
        "easy": ["1+1=?", "2+2=?"],
        "medium": ["12*2=?", "15-5=?"],
        "hard": ["x+3=5, solve x", "2x=8, find x"]
    }

    return random.sample(questions[level], len(questions[level]))
