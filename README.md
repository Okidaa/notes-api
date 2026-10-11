# Notes API

A minimal HTTP service for managing personal notes, built with Python's standard HTTP library for INF 345.

## What it does
- `GET /` - Root status check and available endpoints
- `GET /healthz` - Liveness & readiness healthcheck endpoint
- `GET /notes` - List all notes
- `POST /notes` - Add a new note (JSON payload: `{"text": "your note"}`)

## Port Configuration
The application reads the target HTTP port from the `PORT` environment variable. If not set, it defaults to port `8080`.

## How to run it
```bash
./scripts/run.sh
