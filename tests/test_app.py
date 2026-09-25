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

    @patch("app.urllib.request.urlopen")
    def test_lambda_handler_returns_live_state(self, mock_urlopen):
        mock_urlopen.return_value.__enter__.return_value.read.return_value = json.dumps({
            "gameState": "LIVE",
            "gameScheduleState": "LIVE",
            "startTimeUTC": "2026-09-24T23:00:00Z",
            "easternUTCOffset": "-04:00",
            "venueUTCOffset": "-04:00",
            "venueTimezone": "America/Detroit",
        }).encode("utf-8")

        event = {"gameid": "2025021230"}
        response = app.lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["gameState"], "LIVE")
        self.assertEqual(body["status"], "STARTED")
        self.assertTrue(body["started"])
        self.assertTrue(body["isLive"])
        self.assertEqual(body["gameScheduleState"], "LIVE")
        self.assertEqual(body["venueTimezone"], "America/Detroit")

    @patch("app.urllib.request.urlopen")
    def test_lambda_handler_returns_final_state(self, mock_urlopen):
        mock_urlopen.return_value.__enter__.return_value.read.return_value = json.dumps({
            "gameState": "FINAL",
            "gameScheduleState": "OK",
            "startTimeUTC": "2026-09-24T23:00:00Z",
            "easternUTCOffset": "-04:00",
            "venueUTCOffset": "-04:00",
            "venueTimezone": "America/Detroit",
        }).encode("utf-8")

        event = {"gameid": "2025021231"}
        response = app.lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["gameState"], "FINAL")
        self.assertEqual(body["status"], "ENDED")
        self.assertTrue(body["ended"])
        self.assertFalse(body["isLive"])
        self.assertEqual(body["gameScheduleState"], "OK")
        self.assertEqual(body["startTimeUTC"], "2026-09-24T23:00:00Z")

    def test_lambda_handler_requires_gameid(self):
        response = app.lambda_handler({}, None)

        self.assertEqual(response["statusCode"], 400)
        body = json.loads(response["body"])
        self.assertIn("Missing gameid", body["error"])


if __name__ == "__main__":
    unittest.main()
