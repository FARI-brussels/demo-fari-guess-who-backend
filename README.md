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
