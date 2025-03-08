import openai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env.local')

api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key



def get_explanation(question, answer):
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return completion.choices[0].message['content']