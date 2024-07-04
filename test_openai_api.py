import unittest
from unittest.mock import patch
import openai_api

class TestOpenAIAPI(unittest.TestCase):
    @patch('openai.Completion.create')
    def test_process_question(self, mock_create):
        mock_response = {
            'choices': [{
                'text': 'Alexander\nBeatrice\nCarlos'
            }]
        }
        mock_create.return_value = mock_response

        characters = [
            {"name": "Alexander", "description": "Description of Alexander"},
            {"name": "Beatrice", "description": "Description of Beatrice"},
            {"name": "Carlos", "description": "Description of Carlos"},
            {"name": "Diana", "description": "Description of Diana"}
        ]

        question = "Is the character a man?"
        result = openai_api.process_question(question, characters)
        expected_result = [
            {"name": "Alexander", "description": "Description of Alexander"},
            {"name": "Beatrice", "description": "Description of Beatrice"},
            {"name": "Carlos", "description": "Description of Carlos"}
        ]

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
