# Non-Flat API Documentation

This document describes the nested event structure commonly seen when the Lambda is invoked through API Gateway or a proxied HTTP layer.

## Input shape

```json
{
  "pathParameters": {
    "gameid": "2025021230"
  },
  "queryStringParameters": {
    "gameid": "2025021230"
  }
}
```

The Lambda also accepts a nested case where `gameId` is supplied using a different key casing:

```json
{
  "gameId": "2025021230"
}
```

## Field definitions

- `gameid` or `gameId`: the NHL game ID passed as a top-level key or nested parameter value.
- `pathParameters.gameid`: optional nested value used by API Gateway routes.
- `queryStringParameters.gameid`: optional nested value used by URL query input.

## Expected response

```json
{
  "statusCode": 200,
  "body": "{\"gameid\":\"2025021230\",\"gameState\":\"OFF\",\"gameScheduleState\":\"OK\",\"startTimeUTC\":\"2026-04-06T23:30:00Z\",\"easternUTCOffset\":\"-04:00\",\"venueUTCOffset\":\"-05:00\",\"venueTimezone\":\"America/Winnipeg\",\"status\":\"ENDED\",\"started\":false,\"ended\":true,\"isLive\":false}"
}
```

## Example API Gateway event

```json
{
  "resource": "/game-state/{gameid}",
  "path": "/game-state/2025021230",
  "httpMethod": "GET",
  "pathParameters": {
    "gameid": "2025021230"
  },
  "queryStringParameters": null,
  "headers": {
    "Accept": "application/json"
  }
}
```

## Example error response

```json
{
  "statusCode": 400,
  "body": "{\"error\":\"Missing gameid\"}"
}
```

## Notes

The handler is intentionally tolerant and supports both flat and nested event versions so the same Lambda can work across direct invocation, API Gateway proxy events, and custom integrations.
