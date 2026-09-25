import json
import urllib.request
from typing import Any, Dict, Optional


LIVE_STATES = {"PRE", "LIVE", "CRIT"}
ENDED_STATES = {"OVER", "FINAL", "OFF"}
SCHEDULED_STATES = {"FUT"}


def get_game_state(gameid: str) -> Optional[str]:
    url = f"https://api-web.nhle.com/v1/gamecenter/{gameid}/landing"
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    with urllib.request.urlopen(request, timeout=15) as response:
        payload = json.loads(response.read().decode("utf-8"))

    return payload.get("gameState")


def classify_game_state(game_state: Optional[str]) -> str:
    if game_state in LIVE_STATES:
        return "STARTED"
    if game_state in ENDED_STATES:
        return "ENDED"
    if game_state in SCHEDULED_STATES:
        return "SCHEDULED"
    return "UNKNOWN"


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        if isinstance(event, dict):
            gameid = (
                event.get("gameid")
                or event.get("gameId")
                or event.get("pathParameters", {}).get("gameid")
                or event.get("queryStringParameters", {}).get("gameid")
            )
        else:
            gameid = None

        if not gameid:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing gameid"}),
            }

        url = f"https://api-web.nhle.com/v1/gamecenter/{gameid}/landing"
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))

        game_state = payload.get("gameState") or get_game_state(str(gameid))
        if not game_state:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "gameid": str(gameid),
                    "error": "gameState not found",
                }),
            }

        status = classify_game_state(game_state)

        response_body = {
            "gameid": str(gameid),
            "gameState": game_state,
            "gameScheduleState": payload.get("gameScheduleState"),
            "startTimeUTC": payload.get("startTimeUTC"),
            "easternUTCOffset": payload.get("easternUTCOffset"),
            "venueUTCOffset": payload.get("venueUTCOffset"),
            "venueTimezone": payload.get("venueTimezone"),
            "status": status,
            "started": game_state in LIVE_STATES,
            "ended": game_state in ENDED_STATES,
            "isLive": game_state in {"LIVE", "CRIT"},
        }

        return {
            "statusCode": 200,
            "body": json.dumps(response_body),
        }
    except Exception as exc:  # pragma: no cover - defensive fail path
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(exc)}),
        }
