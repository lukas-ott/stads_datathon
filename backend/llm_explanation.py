import openai
from dotenv import load_dotenv, find_dotenv
import os

env_file = find_dotenv(".env.local")
load_dotenv(env_file)

api_key = os.environ.get("API_KEY")
openai.api_key = api_key

SYSTEM_PROMPT = """You're an auditing assistant, explaining transaction anomalies.
    You will get a dictionary of anomaly reasons and their likelihood of leading to the transaction being labeled an anomaly.
    Your task is to explain the anomaly reason in a way that is understandable to a non-expert.
    The explanation should be concise and easy to understand.
    The explanation should be tailored to the specific anomaly reason and should not be too general.
    The explanation should be written in a way that is easy to understand for a non-expert.
"""


def get_explanation(input_categories: dict[str, float], probability) -> str:
    USER_PROMPT = f"""Anomaly reasons: {input_categories}; Relative probility that given the characteristics, the transaction is an anomaly: {probability}"""
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT},
        ],
    )
    return completion.choices[0].message["content"]



def main():
    input_categories = {
        "Transaction amount is significantly higher than usual": 0.9,
        "Transaction location is unusual": 0.7,
    }
    probability = 0.8
    explanation = get_explanation(input_categories, probability)
    print(explanation)
    
if __name__ == "__main__":
    main()