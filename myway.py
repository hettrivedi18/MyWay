from leaders import leaders
import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


user_profile={"year":input("what year are you in?"),
              "skills":input("what are current skills?"),
              "targeted_role":input("what is your target role?"),
              "dream_company":input("which is your dream company?"),
              "hours_commitment":input("how much hours you are willing to dedicate per week?")}


target = user_profile['targeted_role'].lower()

if 'ai' in target or 'machine learning' in target or 'ml' in target:
    matched_leader = leaders['andrej_karpathy']
elif 'ceo' in target or 'product' in target or 'management' in target:
    matched_leader = leaders['sundar_pichai']
elif 'hardware' in target or 'nvidia' in target:
    matched_leader = leaders['jensen_huang']
elif 'systems' in target or 'backend' in target or 'infrastructure' in target:
    matched_leader = leaders['jeff_dean']
else:
    matched_leader = leaders['satya_nadella']

prompt=f"""I am a year {user_profile['year']} CS student with skills in {user_profile['skills']}. 
My target role is {user_profile['targeted_role']} and my dream company is {user_profile['dream_company']}. 
I can dedicate {user_profile['hours_commitment']} hours per week.

Model my roadmap closely after this real leader's journey:
Name: {matched_leader['role']}
Their path: {matched_leader['path']}
Their key advice: {matched_leader['advice']}
Best for students like: {matched_leader['best_for']}

Start your response by mentioning which leader's path inspired this roadmap and why they match my goals. Then give me a detailed step by step roadmap with career timing and weekly schedule."""

message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(user_profile)
print(message.content[0].text)