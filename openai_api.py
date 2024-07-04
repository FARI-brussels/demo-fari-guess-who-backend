import json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored  
openai.api_key = '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'
GPT_MODEL = "gpt-4o"
client = OpenAI()
def process_question(question, characters):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Question: {question}\n\nCharacters:\n" + "\n".join([f"{c['name']}: {c['description']}" for c in characters]) + "\n\nEliminated characters:",
        max_tokens=150
    )
    eliminated_characters = response.choices[0].text.strip().split('\n')
    return [c for c in characters if c['name'] in eliminated_characters]
