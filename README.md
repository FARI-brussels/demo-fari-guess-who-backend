# Project Name

## Description
This project is a Flask application that interacts with OpenAI's API to generate and process questions based on a set of characters.
The characters are described in characters.json and the questions and attributes used by the AI when playing are described in attribute_questions.json. You can add and remove player by modifying character.json 

## Setup
1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a keys.json file and add your openai api key : 
    ```python
    {"key" : "sk-proj-mykey"}
    ```

## Running the Application
Open a terminal and launch the Flask application, use the following command:
```bash
python app.py
```

And go to http://127.0.0.1:5000 for the player view and http://127.0.0.1:5000/robot_view for the robot view

Open another terminal and use the following command to start the websocket that update the robot screen. 
```bash
python websocket_server.py
```

## API Documentation

### Endpoints

#### `GET /`
- **Description**: Renders the main index page.
- **Response**: HTML content of the index page.

#### `GET /robot_view`
- **Description**: Renders the robot view page.
- **Response**: HTML content of the robot view page.

#### `POST /ask`
- **Description**: Processes a question asked by the player and updates the game state. It returns 
- **Request Body**:
  - `question` (string): The question asked by the player.
- **Response**: JSON object containing:
  - `response` (string): The answer to the question.
  - `remaining_characters` (list): List of remaining characters.
  - `decision_tree` (list): The current decision tree of the player that containing all the question asked in the game, the answer, and how each question split the set of characters
  - `robot_question` (string): The question that the robot ask in turn.
  - `attribute` (string): The attribute related to the robot's question.
  - `value` (string): The value related to the robot's question.
  - `max_gain` (float): The maximum information gain of the robot's question


#### `POST /process_answer`
- **Description**: Processes the player's answer to the robot's question and updates the game state.
- **Request Body**:
  - `attribute` (string): The attribute related to the robot's question.
  - `value` (string): The value related to the robot's question.
  - `response` (string): The player's answer to the robot's question.
  - `robot_question` (string): The robot's question.
  - `max_gain` (float): The maximum information gain.
  
- **Response**: JSON object containing:
  - `response` (object): An object containing:
    - `remaining_characters` (list): List of remaining characters for the robot.
    - `decision_tree` (list): The decision tree of the robot.


## Python code


## Html and Javascript code
## HTML and JavaScript Code

### HTML Files

#### `templates/index.html`
This file contains the main HTML structure for the game interface. It includes sections for displaying character cards, asking and answering questions, and visualizing the decision tree. The file also includes embedded JavaScript for handling form submissions and updating the UI based on responses from the server.

#### `templates/robot_view.html`
This file contains the HTML structure for the robot's view of the game. It displays the character cards and the decision tree. It also includes embedded JavaScript for handling WebSocket messages to update the UI in real-time.

### JavaScript Files

#### `static/create_decision_tree.js`
This file contains the JavaScript code for creating a decision tree visualization using D3.js. The `createDecisionTree` function takes decision tree data as input and generates an interactive tree diagram. The function includes helper functions for building the tree structure and drawing the nodes and links.

## License
This project is licensed under the MIT License.
