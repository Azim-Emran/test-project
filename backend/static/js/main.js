let currentCorrectAnswer = '';
  let currentExplanation = '';
  let currentHint = '';
  let attemptCounter = 0;
  const maxAttempts = 3;
  let chartData = {};

function sendMessage() {
    const inputField = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const message = inputField.value.trim();

    if (!message) return;

    // Append user message
    chatBox.innerHTML += `<div class="text-end"><strong>You:</strong> ${message}</div>`;

    // Send to API
    fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        chatBox.innerHTML += `<div class="text-start"><strong>AI:</strong> ${data.response}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
        inputField.value = '';
    })
    .catch(err => {
        chatBox.innerHTML += `<div class="text-start text-danger"><strong>Error:</strong> Could not get response.</div>`;
    });
}

function detectIntent(message) {
    fetch('/api/detect-intent', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message})
    })
    .then(res => res.json())
    .then(data => {
        console.log("Detected intent:", data.intent);
        // Use intent to guide chatbot logic
    });
}

function askTutor() {
    const question = document.getElementById('gpt-question').value;
    const responseBox = document.getElementById('gpt-response');
    fetch('/api/ask-gpt', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ question, subject: 'math' })
    })
    .then(res => res.json())
    .then(data => {
        responseBox.innerText = data.response;
        responseBox.style.display = 'block';
    });
}


function loadAdaptiveQuestion() {
    fetch('/api/get-adaptive-question')
      .then(res => res.json())
      .then(data => {
        console.log("[DEBUG] Question Data:", data);

        if (data.error || !data.question || !data.answer) {
          alert('❌ Could not load quiz question.');
          return;
        }

        currentCorrectAnswer = data.answer.trim().toLowerCase();
        currentExplanation = data.explanation;
        currentHint = data.hint;
        attemptCounter = 0;

        const contentBox = document.getElementById('question-content');
        contentBox.innerHTML = `
          <p><strong>Q:</strong> ${data.question}</p>
          <input type="text" id="userAnswer" class="form-control mt-2" placeholder="Type your answer..." />
          <button class="btn btn-sm btn-primary mt-2" onclick="submitShortAnswer()">Submit</button>
          <div id="feedback" class="mt-2"></div>
        `;

        document.getElementById('question-box').classList.remove('hidden');
        document.getElementById('question-box').style.display = 'block';
        console.log("✅ Question box should now be visible");
      })
      .catch(err => {
        console.error("[ERROR] Fetch failed:", err);
        alert('❌ Could not load quiz question.');
    });
}

function submitShortAnswer() {
    const input = document.getElementById('userAnswer').value.trim().toLowerCase();
    const feedback = document.getElementById('feedback');

    const isCorrect = input === currentCorrectAnswer;
    const time_taken = Math.floor(Math.random() * 30) + 5;

    fetch('/api/submit-answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_correct: isCorrect, time_taken })
    });

    if (isCorrect) {
        feedback.innerHTML = "<span class='text-success'>✅ Correct!</span>";
    } else {
        feedback.innerHTML = `<span class='text-danger'>❌ Incorrect. Try again.</span><br>
        <strong>Answer:</strong> ${currentCorrectAnswer}<br>
        <strong>Explanation:</strong> ${currentExplanation}`;
    }
}

function getRecommendation() {
    fetch('/api/recommend-topic/1')  // replace with real user ID in production
    .then(res => res.json())
    .then(data => {
        document.getElementById('recommended-topic').innerText =
          `📘 Your next recommended topic is: ${data.recommended_topic}`;
    });
}

fetch('/api/get-progress')
    .then(res => res.json())
    .then(data => {
        const ctx = document.getElementById('progressChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Accuracy (%)',
                    data: data.accuracies,
                    backgroundColor: 'rgba(54,162,235,0.6)'
                }]
            },
            options: {
                scales: { y: { beginAtZero: true, max: 100 } }
            }
        });
    });

    // Layout
document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById("hamburger-menu");
  const nav = document.getElementById("sidebar-nav");

  toggle.addEventListener("click", () => {
    nav.classList.toggle("active");
  });
});
