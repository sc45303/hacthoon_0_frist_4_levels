import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def think(task_text: str) -> str:
    prompt = f"""
You are a Digital AI Employee.

Your job at Bronze level:
- Read the task
- Create a simple step-by-step plan
- Do NOT execute anything

Task:
{task_text}

Respond only with a clear plan.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()
