from flask import Flask, render_template, request
from leaders import leaders
import anthropic
import os
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_profile = {
        'year': request.form['year'],
        'skills': request.form['skills'],
        'targeted_role': request.form['targeted_role'],
        'dream_company': request.form['dream_company'],
        'hours_commitment': request.form['hours_commitment']
    }

    target = user_profile['targeted_role'].lower()

    if any(word in target for word in ['ai', 'ml', 'machine learning', 'data science', 'research']):
        matched_leader = leaders['andrej_karpathy']
    elif any(word in target for word in ['product', 'management', 'ceo', 'founder', 'startup']):
        matched_leader = leaders['sundar_pichai']
    elif any(word in target for word in ['hardware', 'chip', 'gpu', 'nvidia', 'systems']):
        matched_leader = leaders['jensen_huang']
    elif any(word in target for word in ['backend', 'infrastructure', 'distributed', 'engineering']):
        matched_leader = leaders['jeff_dean']
    else:
        matched_leader = leaders['satya_nadella']

    prompt = f"""I am a year {user_profile['year']} CS student with skills in {user_profile['skills']}. 
    My target role is {user_profile['targeted_role']} and my dream company is {user_profile['dream_company']}. 
    I can dedicate {user_profile['hours_commitment']} hours per week.

    Model my roadmap closely after this real leader's journey:
    Name: {matched_leader['role']}
    Their path: {matched_leader['path']}
    Their key advice: {matched_leader['advice']}
    Best for students like: {matched_leader['best_for']}

    You MUST respond with ONLY a JSON object.
    No markdown, no explanation, no code blocks.
    Start your response with {{ and end with }}

    {{
        "leader_name": "full name here",
        "leader_reason": "why this leader matches in 2 sentences",
        "phases": [
            {{"name": "Phase 1", "duration": "Months 1-2", "goal": "goal here", "tasks": ["task1", "task2", "task3"]}}
        ],
        "weekly_schedule": [
            {{"day": "Monday", "hours": 2, "activity": "LeetCode - Arrays"}}
        ],
        "skills_to_cover": ["skill1", "skill2", "skill3", "skill4", "skill5"],
        "milestones": ["milestone1", "milestone2", "milestone3", "milestone4"]
    }}"""

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    clean = raw.replace("```json", "").replace("```", "").strip()
    roadmap_data = json.loads(clean)
    print(roadmap_data)
    return render_template('result.html', data=roadmap_data)

if __name__ == '__main__':
    app.run(debug=True)