import json
import re
from openai import OpenAI
 
 
class MarketAgent:
 
    def __init__(self, client: OpenAI):
        self.client = client
 
        self.system_prompt = """
You are Market Shark.
 
Evaluate startup ideas from a market perspective.
 
Return ONLY valid JSON.
 
{
  "agent": "Market Shark",
  "overall_score": 0,
  "scores": {
    "market_size": 0,
    "problem_severity": 0,
    "solution_quality": 0,
    "traction": 0,
    "competitive_advantage": 0,
    "innovation": 0,
    "scalability": 0
  },
  "strengths": [],
  "weaknesses": [],
  "recommendation": ""
}
"""
 
    def evaluate(self, startup_idea: str):
 
        user_prompt = f"""
Evaluate the following startup idea.
 
Startup Idea:
{startup_idea}
 
Return ONLY valid JSON.
"""
 
        response = self.client.chat.completions.create(
            model="openai.gpt-4o",
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )
 
        content = response.choices[0].message.content.strip()
 
        print("\nMARKET RESPONSE:")
        print(content)
 
        content = re.sub(
            r"^```json\s*",
            "",
            content,
            flags=re.IGNORECASE
        )
 
        content = re.sub(
            r"\s*```$",
            "",
            content
        )
 
        content = content.strip()
 
        return json.loads(content)