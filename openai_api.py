import openai

openai.api_key = 'your_openai_api_key'

def process_question(question, characters):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Question: {question}\n\nCharacters:\n" + "\n".join([f"{c['name']}: {c['description']}" for c in characters]) + "\n\nEliminated characters:",
        max_tokens=150
    )
    eliminated_characters = response.choices[0].text.strip().split('\n')
    return [c for c in characters if c['name'] in eliminated_characters]
