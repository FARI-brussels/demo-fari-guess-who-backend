import json
import openai
from openai import OpenAI, ChatCompletion
from tenacity import retry, wait_random_exponential, stop_after_attempt 

GPT_MODEL = "gpt-4o"
client = OpenAI()
with open("keys.json", "r") as f:
    openai.api_key = json.load(f)["key"]

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={ "type": "json_object" }
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e



def process_question(question, chosen_character, characters):
    messages = [
        {"role": "system", "content": "Eliminate characters based on a question and the character to guess. If the character to guess corresponds to a yes of the question, return the players that also correspond to yes and same with no. Return a JSON with the response of the question and a list of dictionaries containing the name of the remaining characters and a justification for why they were kept. Please don't mention who is the character to guess in the justification. Example: 'response' : 'yes', 'remaining_characters': [{'name': 'tina', 'justification': 'Tina matches is ... because...'}, {'name': 'beatrice', 'justification': 'Beatrice seems to be ... because ...'}]"},
        {"role": "user", "content": f"question: {question}, character to guess: {chosen_character} characters: {characters}"},
    ]
    response = chat_completion_request(messages)
    remaining_characters = json.loads(response.choices[0].message.content)["remaining_characters"]
    response = json.loads(response.choices[0].message.content)["response"]
    return remaining_characters, response


def process_question_and_response(question, response, characters):
    messages = [
        {"role": "system", "content": "Eliminate characters based on a question and a response. If the response is yes, keep only the characters that correspond to a yes answer as well, same for no. Return a JSON with a list of dictionaries containing the name of the remaining characters and a justification for why they were kept. Please don't mention who is the character to guess in the justification. Example: 'remaining_characters': [{'name': 'tina', 'justification': 'Tina matches is ... because...'}, {'name': 'beatrice', 'justification': 'Beatrice seems to be ... because ...'}]"},
        {"role": "user", "content": f"question: {question}, response: {response} characters: {characters}"},
    ]
    response = chat_completion_request(messages)
    remaining_characters = json.loads(response.choices[0].message.content)["remaining_characters"]
    return remaining_characters


def generate_question(remaining_characters):
    messages = [
        {"role": "system", "content": "We are playing guess who, based on the list of remaining characters that I will give you, can you create a question that can be answer by yes or no and split the remaining character in two equal groups. Return a JSON with the generated question."},
        {"role": "user", "content": f"remaining_characters: {remaining_characters}"},
    ]
    response = chat_completion_request(messages)
    question = json.loads(response.choices[0].message.content)["question"]
    return question

