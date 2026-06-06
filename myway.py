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

prompt=f"I am in {user_profile['year']} year, skills I currently have are {user_profile['skills']}, this is my target role  {user_profile['targeted_role']} and  {user_profile['dream_company']} is my dream company, this much hours I am willing to dedicate {user_profile['hours_commitment']} just guide me towards the career I am aiming with proper roadmap and step by step detailing with career timing, also provide weekly schedule according to my hours commitment"

message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(user_profile)
print(message.content[0].text)