async function getRecommendation(state) {
    const res = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ state: state })
    });
    const result = await res.json();
    document.getElementById("recommend-box").innerText = "Recommended: " + result.recommended;
}

async function sendReward(state, action, reward, nextState) {
    await fetch('/api/reward', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ state, action, reward, next_state: nextState })
    });
}

async function submitQuiz(userId, answers, topic, difficulty, grade, previous_avg) {
    const res = await fetch('/api/submit_quiz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: userId,
            answers: answers, // [{question_id, correct: true/false}, ...]
            topic: topic,
            difficulty: difficulty,
            grade: grade,
            previous_avg: previous_avg
        })
    });

    const result = await res.json();
    alert(`Quiz submitted. Score: ${result.score}`);
}
