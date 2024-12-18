from flask import Flask, render_template, request, jsonify
import random
import json
import openai_api
import os
import evaluate_information_gain

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Load characters and attribute questions from JSON files
with open('characters.json', 'r') as f:
    characters = json.load(f)

with open('attribute_questions.json', 'r') as f:
    attribute_questions = json.load(f)

# Function to initialize the game state
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

# Function to filter characters based on the remaining characters
def filter_characters(initial_list, remaining_characters):
    return [character for character in initial_list if any(rc['name'] == character['name'] for rc in remaining_characters)]

# Function to update the decision tree with the latest question and answer
def update_decision_tree(decision_tree, question, answer, information_gain, response):
    if answer == "no":
        not_answer = "yes"
    else:
        not_answer = "no"
    decision_tree.append({
        "question": question,
        "response": answer,
        "information_gain": information_gain,
        not_answer: [r for r in response if r['answer'] == not_answer],
        answer: [r for r in response if r['answer'] == answer]
    })
    print(decision_tree)
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
    response = openai_api.process_question(question, chosen_character, remaining_characters_player)
    answer = next(item["answer"] for item in response if item['name'] == chosen_character['name'])
    remaining_characters = [char for char in response if char["answer"] == answer]
    eliminated_characters = [char for char in response if char["answer"] != answer]
    filtered = filter_characters(characters, remaining_characters)
    information_gain = evaluate_information_gain.calculate_weighted_information_gain(remaining_characters_player, len([char['name'] for char in remaining_characters if char not in filtered]),len([char['name'] for char in filtered]) )
    _, __, ___, max_information_gain = evaluate_information_gain.generate_best_question(remaining_characters_player, attribute_questions)
    decision_tree_player = update_decision_tree(decision_tree_player, question, answer, information_gain , response)
    remaining_characters_player = filtered
    robot_question, best_attribute, best_value, max_gain = evaluate_information_gain.generate_best_question(remaining_characters_robot, attribute_questions)
    resp = {
        "response": answer,
        "remaining_characters": remaining_characters,
        "eliminated_charaters": eliminated_characters,
        "decision_tree": decision_tree_player,
        "robot_question": robot_question, 
        "attribute": best_attribute,
        "value": best_value, 
        "max_gain" : max_gain
    }
    return jsonify(resp)

@app.route('/process_answer', methods=['POST'])
def process_answer():
    global remaining_characters_robot
    global decision_tree_robot
    data = request.json
    attribute = data['attribute']
    value = data['value']
    answer = data['response']
    question = data['robot_question']
    information_gain = data['max_gain']
    remaining_characters, response = evaluate_information_gain.process_question(attribute, value, answer, remaining_characters_robot)
    filtered = filter_characters(remaining_characters_robot, remaining_characters)
    decision_tree_robot = update_decision_tree(decision_tree_robot, question, answer, information_gain, response)
    remaining_characters_robot = filtered
    # Save the remaining characters and decision tree to a JSON file
    with open('robot_state.json', 'w') as f:
        json.dump({
            "remaining_characters": remaining_characters_robot,
            "decision_tree": decision_tree_robot, 
        }, f)

    return jsonify({"response": {"remaining_characters": remaining_characters_robot, "decision_tree": decision_tree_robot}})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
