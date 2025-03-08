import openai
from dotenv import load_dotenv
import os
import anomaly_categorization

load_dotenv(".env.local")
api_key = os.environ.get("API_KEY")
openai.api_key = api_key

SYSTEM_PROMPT = f"""
    You're an auditing assistant, explaining transaction anomalies.
    You will get a dictionary of anomaly reasons and their likelihood of leading to the transaction being labeled an anomaly.
    Your task is to explain the anomaly reason in a way that is understandable to a non-expert.
    The explanation should be concise and easy to understand.
    The explanation should be tailored to the specific anomaly reason and should not be too general.
    The explanation should be written in a way that is easy to understand for a non-expert.
    The explanation should start with the first variable possibly leading to a anomaly.
    After that it should entail the explanation followed by the probability in % that a transaction with this characteristic is an anomaly.
    For the keys 'WRBTR_H' and 'DMBTR_H' please take the second interval from the dedection metrics.
    For the keys 'WRBTR_L' and 'DMBTR_L' please take the first interval from the dedection metrics.
    

    Now I will explain a second dictionary that does not contain all found anomalies but all anomalies that could be found.
    This is the dict:
    {anomaly_categorization.anomaly_categories}
    The name of the variable/ field that contains a susicious value is the key of another dictionary.
    In the other dictionary a level deeper you will find information about the explanation and the detection metrics.
    Please explain why the transaction is labeled as an anomaly. Information about that can be found after the label 'explanation' in the input we give to you.
    Mostly that are sets of discret values where the variables is not an element of or a continious interval where the variable is an element of.
    Please use the detection metrics to further detail the explanation so that the auditor knows why his value could be false that he put in.

    Example:
    1. WRBTR: The value is suspicious because it is in the interval 544E2 to 545E2. There the majority of transactions are anomalies. The probabilty of a transaction being an anomaly with this characteristic is 84%.
    2. WAERS: The value is suspicious because it is not one of the following that contain mostly regular transactions: [C1 to C9]. Outside this set the majority of transactions are anomalies. The probabilty of a transaction being an anomaly with this characteristic is 50%.
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