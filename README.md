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

4. Set your OpenAI API key in the `openai_api.py` file:
    ```python
    openai.api_key = 'your_openai_api_key'
    ```

## Running the Application
To run the Flask application, use the following command:
```bash
flask run
```

## Running the Tests
To run the tests, use the following command:
```bash
python -m unittest discover
```

This will discover and run all the tests in the `test_app.py` file.

## License
This project is licensed under the MIT License.
