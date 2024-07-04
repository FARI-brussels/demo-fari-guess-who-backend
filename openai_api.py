import json
from openai import OpenAI, ChatCompletion
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored  
openai.api_key = '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'
GPT_MODEL = "gpt-4o"
client = OpenAI()
tools = [
    {
        "type": "function",
        "function": {
            "name": "eliminate_characters",
            "description": "Eliminate characters based on the question",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question asked by the user",
                    },
                    "characters": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "description": {"type": "string"},
                            },
                            "required": ["name", "description"],
                        },
                        "description": "List of characters with their descriptions",
                    },
                },
                "required": ["question", "characters"],
            },
        }
    }
]

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def process_question(question, characters):
    messages = [
        {"role": "system", "content": "Eliminate characters based on the question."},
        {"role": "user", "content": question},
        {"role": "function", "name": "eliminate_characters", "content": json.dumps({"question": question, "characters": characters})}
    ]
    response = chat_completion_request(messages, tools=tools)
    eliminated_characters = json.loads(response.choices[0].message["function_call"]["arguments"])["eliminated_characters"]
    return [c for c in characters if c['name'] in eliminated_characters]
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Question: {question}\n\nCharacters:\n" + "\n".join([f"{c['name']}: {c['description']}" for c in characters]) + "\n\nEliminated characters:",
        max_tokens=150
    )
    eliminated_characters = response.choices[0].text.strip().split('\n')
    return [c for c in characters if c['name'] in eliminated_characters]
