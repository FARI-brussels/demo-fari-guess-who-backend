# Project Name

## Description
This project is a Flask application that interacts with OpenAI's API to generate and process questions based on a set of characters.

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


## License
This project is licensed under the MIT License.
## API Documentation

### Endpoints

#### `GET /`
- **Description**: Renders the main index page.
- **Response**: HTML content of the index page.

#### `GET /robot_view`
- **Description**: Renders the robot view page.
- **Response**: HTML content of the robot view page.

#### `POST /ask`
- **Description**: Processes a question asked by the player and updates the game state.
- **Request Body**:
  - `question` (string): The question asked by the player.
- **Response**: JSON object containing:
  - `response` (string): The answer to the question.
  - `remaining_characters` (list): List of remaining characters.
  - `decision_tree` (list): The decision tree of the player.
  - `robot_question` (string): The question generated for the robot.
  - `attribute` (string): The attribute related to the robot's question.
  - `value` (string): The value related to the robot's question.
  - `max_gain` (float): The maximum information gain.

#### `POST /process_answer`
- **Description**: Processes the player's answer to the robot's question and updates the game state.
- **Request Body**:
  - `attribute` (string): The attribute related to the robot's question.
  - `value` (string): The value related to the robot's question.
  - `response` (string): The player's answer to the robot's question.
  - `question` (string): The robot's question.
  - `max_gain` (float): The maximum information gain.
- **Response**: JSON object containing:
  - `response` (object): An object containing:
    - `remaining_characters` (list): List of remaining characters for the robot.
    - `decision_tree` (list): The decision tree of the robot.
