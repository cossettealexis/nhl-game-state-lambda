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

## Field definitions

- `gameid`: NHL game identifier
- `gameState`: current NHL lifecycle state
- `gameScheduleState`: schedule state from the NHL landing payload
- `startTimeUTC`: start time in UTC
- `easternUTCOffset`: Eastern time offset
- `venueUTCOffset`: venue local offset from UTC
- `venueTimezone`: venue IANA timezone name
- `status`: normalized lifecycle status (`STARTED`, `ENDED`, `SCHEDULED`, `UNKNOWN`)
- `started`: true when the game is in a started state
- `ended`: true when the game is in an ended state
- `isLive`: true only for live/critical states

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

## Example error response

```json
{
  "statusCode": 400,
  "body": "{\"error\":\"Missing gameid\"}"
}
```
