import json
import openai
from openai import OpenAI, ChatCompletion
from tenacity import retry, wait_random_exponential, stop_after_attempt 

GPT_MODEL = "gpt-4o"


with open("keys.json", "r") as f:
    api_key = json.load(f)["key"]
    client = OpenAI(api_key=api_key)

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
        {"role": "system", "content": "We are playing the guess who game, can you please classify the following characters based on the question and the character to guess that I will give you. Please Return a JSON list with the character, the answer of the question for that characters and a justification for why this answer was chosen The answer can only be yes or no. Please don't mention who is the character to guess in the justification. Example: 'response' : [{'name': 'tina', 'answer': 'yes', 'justification': 'Tina matches  ... because...'}, {'name': 'beatrice', 'answer', 'no', 'justification': 'Beatrice seems to be ... because ...'}, ....]"},
        {"role": "user", "content": f"question: {question}, character to guess: {chosen_character} characters: {characters}"},
    ]
    response = json.loads(chat_completion_request(messages).choices[0].message.content)["response"]
    return response


def process_question_and_response(question, response, characters):
    messages = [
        {"role": "system", "content": "Eliminate characters based on a question and a response. If the response is yes, keep only the characters that correspond to a yes answer as well, same for no. Return a JSON with a list of dictionaries containing the name of the remaining characters and a justification for why they were kept. Please don't mention who is the character to guess in the justification. Example: 'remaining_characters': [{'name': 'tina', 'justification': 'Tina matches is ... because...'}, {'name': 'beatrice', 'justification': 'Beatrice seems to be ... because ...'}]"},
        {"role": "user", "content": f"question: {question}, response: {response} characters: {characters}"},
    ]
    response = chat_completion_request(messages)
    remaining_characters = json.loads(response.choices[0].message.content)["remaining_characters"]
    return remaining_characters


def generate_question(remaining_characters, previous_questions):
    messages = [
        {"role": "system", "content": "We are playing guess who, based on the list of remaining characters that I will give you, can you create a question that can be answer by yes or no and split the remaining character in two equal groups. Please don't ask a question related to the previous questions. Return a JSON with the generated question. example : {'question' : 'is it a man ?'}"},
        {"role": "user", "content": f"remaining_characters: {remaining_characters}, previous questions :{previous_questions}"},
    ]
    
    response = chat_completion_request(messages)
    question = json.loads(response.choices[0].message.content)["question"]
    return question

