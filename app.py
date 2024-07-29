from flask import Flask, render_template, request, jsonify
import random
import json
import openai_api
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

with open('characters.json', 'r') as f:
    characters = json.load(f)

def initialize_game():

    chosen_character = random.choice(characters)
    remaining_characters_player = characters.copy()
    remaining_characters_robot = characters.copy()
    decision_tree_player = []
    decision_tree_robot = []
    if os.path.exists("/tmp/robot_state.json"):
        # Delete the file
        os.remove("/tmp/robot_state.json")
    return chosen_character, remaining_characters_player, remaining_characters_robot, decision_tree_player, decision_tree_robot

def filter_characters(initial_list, remaining_characters):
    return [character for character in initial_list if any(rc['name'] == character['name'] for rc in remaining_characters)]

def update_decision_tree(decision_tree, question, answer, filtered, remaining_characters):
    if answer in "no":
        not_answer = "yes"
    else:
        not_answer = "no"
    decision_tree.append({
        "question": question,
        "response": answer,
        not_answer: [char['name'] for char in remaining_characters if char not in filtered],
        answer: [char['name'] for char in filtered]
    })
    return decision_tree

@app.route('/')
def index():
    global chosen_character, remaining_characters_player, remaining_characters_robot, decision_tree_player, decision_tree_robot
    chosen_character, remaining_characters_player, remaining_characters_robot, decision_tree_player, decision_tree_robot = initialize_game()
    return render_template('index.html', characters=characters)

@app.route('/robot_view')
def robot_view():
    return render_template('robot_view.html', characters=characters)


@app.route('/ask', methods=['POST'])
def ask():
    global chosen_character
    global remaining_characters_player
    global remaining_characters_robot
    global decision_tree_player
    data = request.json
    question = data['question']
    remaining_characters, answer = openai_api.process_question(question, chosen_character, remaining_characters_player)
    filtered = filter_characters(characters, remaining_characters)
    decision_tree_player = update_decision_tree(decision_tree_player, question, answer, filtered, remaining_characters_player)
    remaining_characters_player = filtered
    resp = {
        "response": answer,
        "remaining_characters": remaining_characters,
        "decision_tree": decision_tree_player,
        "robot_question": openai_api.generate_question(remaining_characters_robot, [item['question'] for item in decision_tree_robot])
    }
    return jsonify(resp)

@app.route('/process_answer', methods=['POST'])
def process_answer():
    global remaining_characters_robot
    global decision_tree_robot
    data = request.json
    question = data['question']
    answer = data['response']
    remaining_characters, _ = openai_api.process_question(question, answer, remaining_characters_robot)
    filtered = filter_characters(remaining_characters_robot, remaining_characters)
    decision_tree_robot = update_decision_tree(decision_tree_robot, question, answer, filtered, remaining_characters_robot)
    
    remaining_characters_robot = filtered
    
    # Save the remaining characters and decision tree to a JSON file
    with open('/tmp/robot_state.json', 'w') as f:
        json.dump({
            "remaining_characters": remaining_characters_robot,
            "decision_tree": decision_tree_robot
        }, f)

    return jsonify({"response": {"remaining_characters": remaining_characters_robot, "decision_tree": decision_tree_robot}})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)