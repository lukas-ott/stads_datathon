import openai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.local")

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

SYSTEM_PROMPT = """You're an auditing assistant, explaining transaction anomalies.
    You will get a dictionary of anomaly reasons and their likelihood of leading to the transaction being labeled an anomaly.
    Your task is to explain the anomaly reason in a way that is understandable to a non-expert.
    The explanation should be concise and easy to understand.
    The explanation should be tailored to the specific anomaly reason and should not be too general.
    The explanation should be written in a way that is easy to understand for a non-expert.
"""


def get_explanation(input_categories: dict[str, float]) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": input_categories},
        ],
    )
    return completion.choices[0].message["content"]
