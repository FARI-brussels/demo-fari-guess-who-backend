import unittest
from flask import Flask
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_ask_route(self):
        question = "Is the character a man?"
        response = self.app.post('/ask', json={'question': question}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_generate_question_route(self):
        response = self.app.post('/ask', json={}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('question', data)
        self.assertIsInstance(data['question'], str)
    unittest.main()
