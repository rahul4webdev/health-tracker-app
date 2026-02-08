#!/bin/bash
set -e

# Health Tracker API — Process Start Script
# Used by GitHub Actions deploy workflow to start/restart the API.

APP_DIR="/home/healthapi.gahfaudio.in/public_html"
PORT=8022
LOG_FILE="${APP_DIR}/api.log"

cd "$APP_DIR"

# Activate virtual environment
source venv/bin/activate

# Kill any existing uvicorn process for this app
pkill -f "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}" || true
sleep 2

# Start uvicorn in the background with logging
nohup venv/bin/uvicorn app.main:app \
  --host 0.0.0.0 \
  --port "$PORT" \
  --log-level info \
  > "$LOG_FILE" 2>&1 &

echo "API server started on port ${PORT} (PID: $!)"
echo "Logs: ${LOG_FILE}"
