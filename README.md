# NHL Game State Lambda

This Lambda returns the current NHL lifecycle state for a provided game ID.

It is designed for direct upload to AWS Lambda with no external dependencies. The implementation uses the standard Python library only.

## Overview

Endpoint used:

- https://api-web.nhle.com/v1/gamecenter/{gameid}/landing

Important fields from the NHL payload:

- `gameState`
  - `FUT`: scheduled
  - `PRE`: pregame / warmups
  - `LIVE`: game in progress
  - `CRIT`: critical live moment
  - `OVER`: game ended, soft final state
  - `FINAL`: final
  - `OFF`: official/finalized

Classification used by this Lambda:

- Started: `PRE`, `LIVE`, `CRIT`
- Ended: `OVER`, `FINAL`, `OFF`
- Scheduled: `FUT`
- Unknown: anything else

## Direct upload

Upload the contents of `lambda_function.py` as the Lambda handler.

Handler:

- `lambda_handler`

## Request contract

The Lambda accepts a `gameid` value in either of these forms:

1. Flat request object
2. Nested API Gateway-style object

See the documentation below for both formats:

- [docs/api-flat.md](docs/api-flat.md)
- [docs/api-nonflat.md](docs/api-nonflat.md)

## Example flat request

```json
{
  "gameid": "2025021230"
}
```

## Example response

```json
{
  "gameid": "2025021230",
  "gameState": "OFF",
  "gameScheduleState": "OK",
  "startTimeUTC": "2026-04-06T23:30:00Z",
  "easternUTCOffset": "-04:00",
  "venueUTCOffset": "-05:00",
  "venueTimezone": "America/Winnipeg",
  "status": "ENDED",
  "started": false,
  "ended": true,
  "isLive": false
}
```

Additional NHL metadata returned by the landing payload:

- `gameScheduleState`
- `startTimeUTC`
- `easternUTCOffset`
- `venueUTCOffset`
- `venueTimezone`

## Response behavior

The function returns:

- HTTP 200 when a valid NHL game state is returned
- HTTP 400 when the `gameid` is missing
- HTTP 404 when the NHL response does not include `gameState`
- HTTP 500 when the request fails or an unexpected exception occurs

## AWS Lambda deployment

Use the file `lambda_function.py` as the full Lambda source.

### 1. Create the Lambda in AWS

In AWS Lambda:

- Create a new Python Lambda function
- Runtime: Python 3.12 or later
- Architecture: x86_64 or arm64 depending on your preference
- Upload the contents of `lambda_function.py` as the function code
- Set the handler to:

```python
lambda_function.lambda_handler
```

### 2. Configure permissions

The function only needs outbound network access to call the NHL public API. No AWS SDK or database is required.

### 3. Test the Lambda in AWS console

Use this test event:

```json
{
  "gameid": "2025021230"
}
```

Expected response:

```json
{
  "statusCode": 200,
  "body": "{\"gameid\":\"2025021230\",\"gameState\":\"OFF\",\"gameScheduleState\":\"OK\",\"startTimeUTC\":\"2026-04-06T23:30:00Z\",\"easternUTCOffset\":\"-04:00\",\"venueUTCOffset\":\"-05:00\",\"venueTimezone\":\"America/Winnipeg\",\"status\":\"ENDED\",\"started\":false,\"ended\":true,\"isLive\":false}"
}
```

### 4. API Gateway integration

If you expose this through API Gateway, the same Lambda accepts a nested event shape too:

```json
{
  "pathParameters": {
    "gameid": "2025021230"
  }
}
```

or:

```json
{
  "queryStringParameters": {
    "gameid": "2025021230"
  }
}
```

### 5. Example Lambda invocation from CLI

```bash
aws lambda invoke \
  --function-name your-function-name \
  --payload '{"gameid":"2025021230"}' \
  response.json

cat response.json
```

### 6. Example API Gateway HTTP call

```bash
curl "https://your-api-id.execute-api.us-east-1.amazonaws.com/prod?gameid=2025021230"
```

## Files in this folder

- `lambda_function.py`: direct-upload Lambda entry point
- `app.py`: local/test-friendly version of the same logic
- `tests/test_app.py`: unit tests for classification and Lambda response handling

## Notes

This wrapper is intentionally minimal and returns only the game state needed for monitoring.

It does not return the full play-by-play feed unless that is added later as a separate endpoint or separate Lambda.
