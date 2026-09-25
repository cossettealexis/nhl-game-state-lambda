# Flat API Documentation

This document describes the flat request format expected by the Lambda.

## Input shape

```json
{
  "gameid": "2025021230"
}
```

## Field definitions

- `gameid` (required): NHL game identifier used in the URL.

Example:

```json
{
  "gameid": "2025021230"
}
```

## Expected response

```json
{
  "gameid": "2025021230",
  "gameState": "LIVE",
  "status": "STARTED",
  "started": true,
  "ended": false,
  "isLive": true
}
```

## Status meanings

- `STARTED`: `PRE`, `LIVE`, or `CRIT`
- `ENDED`: `OVER`, `FINAL`, or `OFF`
- `SCHEDULED`: `FUT`
- `UNKNOWN`: unrecognized or missing NHL state

## Example success response

```json
{
  "gameid": "2025021231",
  "gameState": "FINAL",
  "status": "ENDED",
  "started": false,
  "ended": true,
  "isLive": false
}
```

## Example error response

```json
{
  "statusCode": 400,
  "body": "{\"error\":\"Missing gameid\"}"
}
```
