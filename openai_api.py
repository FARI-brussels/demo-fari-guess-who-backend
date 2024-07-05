import json
import openai
from openai import OpenAI, ChatCompletion
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored  
openai.api_key = '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'
GPT_MODEL = "gpt-4o"
client = OpenAI()

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
        {"role": "system", "content": "Eliminate characters based on the question and the chosen character. If the choosen character correspond to a yes of the question, return the player that also correspond to yes and same with no. Return a json with a list of name of the remaining charaters Example : 'remaining_characters' : ['tina', 'bratrice', 'fred']'"},
        {"role": "user", "content": f"question: {question}, chosen_character: {chosen_character} characters: {characters}"},
    ]
    response = chat_completion_request(messages)
    print(response)
    remaining_characters = response.choices[0].message.content
    return json.loads(remaining_characters)["remaining_characters"]