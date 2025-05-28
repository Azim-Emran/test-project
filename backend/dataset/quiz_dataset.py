import json

quiz_data = [
    {
        "topic": "Solving Linear Equations",
        "level": "Beginner",
        "questions": [
            {
                "question": "Solve for x: 2x + 3 = 11",
                "answer": "x = 4",
                "explanation": "Subtract 3 then divide by 2: (11 - 3)/2 = 4"
            },
            {
                "question": "What is the value of x in 3x = 12?",
                "answer": "x = 4", # Needs to put "4" as well
                "explanation": "Divide both sides by 3: 12 / 3 = 4"
            }
        ]
    },
    {
        "topic": "Understanding Angles",
        "level": "Beginner",
        "questions": [
            {
                "question": "What is the sum of the angles in a triangle?",
                "answer": "180°",
                "explanation": "The sum of the interior angles in any triangle is 180°."
            }
        ]
    }
]

# Save to file
with open('quiz_dataset.json', 'w') as f:
    json.dump(quiz_data, f, indent=4)
