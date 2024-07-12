from flask import Flask, render_template, request, jsonify
import openai_api
import random

app = Flask(__name__)

characters = [
    {"name": "Alexander", "description": "Alexander is a tall man with glasses and a neatly trimmed beard. He has short, brown hair and is often seen wearing a blue suit with a red tie. His eyes are green, and he has a slight dimple on his left cheek when he smiles."},
    {"name": "Beatrice", "description": "Beatrice is a woman with curly red hair that reaches her shoulders. She wears a pair of small, round glasses and has a friendly, warm smile. Her favorite outfit is a yellow dress with floral patterns, and she often accessorizes with a green scarf."},
    {"name": "Carlos", "description": "Carlos is a middle-aged man with a bald head and a thick mustache. He has dark brown eyes and usually wears a white shirt with suspenders. He has a hearty laugh and is known for his jovial personality."},
    {"name": "Diana", "description": "Diana has long, straight black hair and deep blue eyes. She often wears a stylish purple blazer and matching skirt. She has a slender figure and is known for her elegance and poise."},
    {"name": "Edward", "description": "Edward has salt-and-pepper hair and a clean-shaven face. He wears a pair of rectangular glasses and is often seen in a green cardigan and khaki pants. He has a calm demeanor and is always carrying a book."},
    {"name": "Fiona", "description": "Fiona has short, spiky blonde hair and bright blue eyes. She is athletic and often seen in a red tracksuit. She has a confident smile and is known for her energetic nature."},
    {"name": "George", "description": "George has a thick head of curly brown hair and a matching beard. He has hazel eyes and wears a blue flannel shirt with jeans. He has a rugged look and often carries a camera."},
    {"name": "Hannah", "description": "Hannah has long, wavy brown hair and light brown eyes. She often wears a pink sweater and denim jeans. She has a friendly smile and is known for her kindness."},
    {"name": "Isaac", "description": "Isaac is a young man with short black hair and a clean-shaven face. He wears a pair of aviator sunglasses and a leather jacket. He has a mysterious aura and often carries a motorcycle helmet."},
    {"name": "Jessica", "description": "Jessica has medium-length auburn hair and green eyes. She wears a white blouse with a black skirt and a red belt. She has a professional look and is known for her intelligence."},
    {"name": "Kevin", "description": "Kevin has a buzz cut and piercing blue eyes. He is often seen in a grey hoodie and jeans. He has a casual style and is known for his quick wit."},
    {"name": "Lily", "description": "Lily has long, blonde hair tied in a ponytail and blue eyes. She wears a light green dress and a sunhat. She has a cheerful personality and loves gardening."},
    {"name": "Michael", "description": "Michael has short, blonde hair and blue eyes. He wears a red polo shirt and beige shorts. He has a sporty look and is known for his competitive spirit."},
    {"name": "Natalie", "description": "Natalie has short, straight black hair and brown eyes. She wears a white t-shirt with a black leather jacket. She has a rebellious look and loves playing the guitar."},
    {"name": "Oscar", "description": "Oscar has a full head of grey hair and a well-trimmed beard. He wears a brown sweater and corduroy pants. He has a grandfatherly appearance and is always smiling."},
    {"name": "Penelope", "description": "Penelope has long, curly blonde hair and blue eyes. She wears a purple dress and a pearl necklace. She has a graceful look and is known for her artistic talent."},
    {"name": "Quentin", "description": "Quentin has short, black hair and dark brown eyes. He wears a white shirt with a black vest and tie. He has a sharp look and is known for his charisma."},
    {"name": "Rachel", "description": "Rachel has shoulder-length red hair and green eyes. She wears a blue blouse with a floral scarf. She has a friendly smile and loves animals."},
    {"name": "Samuel", "description": "Samuel has curly brown hair and hazel eyes. He wears a plaid shirt and jeans. He has a laid-back style and enjoys outdoor activities."},
    {"name": "Tina", "description": "Tina has short, curly black hair and dark brown eyes. She wears a yellow t-shirt and blue jeans. She has an energetic personality and loves dancing."}
]


def filter_characters(initial_list, remaining_characters):
    return [character for character in initial_list if any(rc['name'] == character['name'] for rc in remaining_characters)]

def update_decision_tree(decision_tree, question, response, remaining_caracters):

    decision_tree.append({
        "question": question,
        "yes": [char['name'] for char in remaining_caracters if char not in response],
        "no": [char['name'] for char in response]
    })
    return decision_tree


def initialize_game():
    chosen_character = random.choice(characters)
    remaining_characters_player = characters.copy()
    remaining_characters_robot = characters.copy()
    decision_tree_player = []
    decision_tree_robot = []
    return chosen_character, remaining_characters_player, remaining_characters_robot, decision_tree_player, decision_tree_robot

@app.route('/')
def index():
    global chosen_character, remaining_characters_player, remaining_characters_robot, decision_tree_player, decision_tree_robot
    chosen_character, remaining_characters_player, remaining_characters_robot, decision_tree_player, decision_tree_robot = initialize_game()
    return render_template('index.html', characters=characters)

@app.route('/robot_view', methods=['POST'])
def robot_view():
    return render_template('robot_view.html', characters=characters)

@app.route('/robot_view', methods=['POST'])
def robot_view():
    return render_template('robot_view.html', characters=characters)

def generate_question(remaining_characters):
    return f"Is your character {remaining_characters[0]['description']}?"

@app.route('/ask', methods=['POST'])
def ask():
    global chosen_character
    global remaining_characters_player
    global remaining_characters_robot
    global decision_tree_player
    data = request.json
    question = data['question']
    remaning_characters, response = openai_api.process_question(question, chosen_character, remaining_characters_player)
    filtered = filter_characters(characters, remaning_characters)
    decision_tree_player = update_decision_tree(decision_tree_player, question, filtered, remaining_characters_player)
    remaining_characters_player = filtered
    resp = {
        "response": response,
        "remaining_characters": remaning_characters,
        "decision_tree": decision_tree_player,
        "robot_question": openai_api.generate_question(remaining_characters_robot)
    }
    return jsonify(resp)

"""
@app.route('/generate_question', methods=['GET'])
def generate_question():
    global remaining_characters_robot
    question = openai_api.generate_question(remaining_characters_robot)
    response = {
        "question": question
    }
    return jsonify(response)
"""

@app.route('/process_answer', methods=['POST'])
def process_answer():
    global remaining_characters_robot
    global decision_tree_robot
    data = request.json
    question = data['question']
    response = data['response']
    resp = openai_api.process_question_and_response(question, response, remaining_characters_robot)
    filtered = filter_characters(remaining_characters_robot, resp)
    decision_tree_robot = update_decision_tree(decision_tree_robot , question, filtered , remaining_characters_robot)
    response = {
        "response": resp,
        "decision_tree": decision_tree_robot
    }
    return jsonify({"response": response})
    

if __name__ == '__main__':
    app.run(debug=True)
