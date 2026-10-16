import json
import re
from openai import OpenAI
 
 
class FinanceAgent:
 
    def __init__(self, client: OpenAI):
 
        self.client = client
 
        self.system_prompt = """
You are Finance Shark.
 
Return ONLY valid JSON.
 
{
  "agent": "Finance Shark",
  "overall_score": 0,
  "scores": {
    "revenue_potential": 0,
    "business_model_strength": 0,
    "profitability_potential": 0,
    "cost_structure": 0,
    "funding_requirements": 0,
    "recurring_revenue": 0,
    "financial_scalability": 0
  },
  "strengths": [],
  "weaknesses": [],
  "recommendation": ""
}
"""
 
    def evaluate(self, startup_idea: str):
 
        user_prompt = f"""
Evaluate the startup.
 
Startup Idea:
{startup_idea}
 
Return ONLY JSON.
"""
 
        response = self.client.chat.completions.create(
            model="openai.gpt-4o",
            temperature=0.3,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
 
        content = response.choices[0].message.content.strip()
 
        print("\nFINANCE RESPONSE:")
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