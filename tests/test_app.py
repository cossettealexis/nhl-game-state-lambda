import json
import unittest
from unittest.mock import patch

import app


class TestNhlGameStateLambda(unittest.TestCase):
    def test_classify_game_state_live(self):
        self.assertEqual(app.classify_game_state("LIVE"), "STARTED")
        self.assertEqual(app.classify_game_state("CRIT"), "STARTED")
        self.assertEqual(app.classify_game_state("PRE"), "STARTED")

    def test_classify_game_state_ended(self):
        self.assertEqual(app.classify_game_state("FINAL"), "ENDED")
        self.assertEqual(app.classify_game_state("OVER"), "ENDED")
        self.assertEqual(app.classify_game_state("OFF"), "ENDED")

    def test_classify_game_state_scheduled(self):
        self.assertEqual(app.classify_game_state("FUT"), "SCHEDULED")

    def test_classify_game_state_unknown(self):
        self.assertEqual(app.classify_game_state("UNKNOWN_STATE"), "UNKNOWN")
        self.assertEqual(app.classify_game_state(None), "UNKNOWN")

    @patch("app.get_game_state")
    def test_lambda_handler_returns_live_state(self, mock_get_game_state):
        mock_get_game_state.return_value = "LIVE"

        event = {"gameid": "2025021230"}
        response = app.lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["gameState"], "LIVE")
        self.assertEqual(body["status"], "STARTED")
        self.assertTrue(body["started"])
        self.assertTrue(body["isLive"])

    @patch("app.get_game_state")
    def test_lambda_handler_returns_final_state(self, mock_get_game_state):
        mock_get_game_state.return_value = "FINAL"

        event = {"gameid": "2025021231"}
        response = app.lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["gameState"], "FINAL")
        self.assertEqual(body["status"], "ENDED")
        self.assertTrue(body["ended"])
        self.assertFalse(body["isLive"])

    def test_lambda_handler_requires_gameid(self):
        response = app.lambda_handler({}, None)

        self.assertEqual(response["statusCode"], 400)
        body = json.loads(response["body"])
        self.assertIn("Missing gameid", body["error"])


if __name__ == "__main__":
    unittest.main()
