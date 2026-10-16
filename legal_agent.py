import json
import re
from openai import OpenAI
 
 
class LegalAgent:
 
    def __init__(self, client: OpenAI):
 
        self.client = client
 
        self.system_prompt = """
You are Legal Shark.
 
Return ONLY valid JSON.
 
{
  "agent": "Legal Shark",
  "overall_score": 0,
  "scores": {
    "regulatory_risk": 0,
    "data_privacy_risk": 0,
    "compliance_complexity": 0,
    "ip_defensibility": 0,
    "employment_law_exposure": 0,
    "litigation_risk": 0,
    "market_accessibility": 0
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
 
        print("\nLEGAL RESPONSE:")
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
