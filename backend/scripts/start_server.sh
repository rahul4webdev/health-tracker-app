#!/bin/bash
set -e

# Health Tracker API — Service Management Script
# Used by GitHub Actions workflow and manual recovery.
# Delegates to systemd for process management and crash recovery.

SERVICE_NAME="health-tracker-api"
PORT=8022
MAX_WAIT=30

echo "=== Health Tracker API — Start/Restart ==="

# Stop any stale nohup uvicorn processes (legacy cleanup)
pkill -f "uvicorn app.main:app.*--port ${PORT}" 2>/dev/null || true
sleep 1

# Restart via systemd (provides Restart=always for crash recovery)
echo "Restarting ${SERVICE_NAME} via systemd..."
systemctl restart "$SERVICE_NAME"

# Wait for the service to become healthy
echo "Waiting for API to become healthy (max ${MAX_WAIT}s)..."
for i in $(seq 1 "$MAX_WAIT"); do
  if curl -sf http://127.0.0.1:${PORT}/health > /dev/null 2>&1; then
    echo "API is healthy after ${i}s"
    echo "Service status:"
    systemctl is-active "$SERVICE_NAME"
    exit 0
  fi
  sleep 1
done

# If we get here, startup failed
echo "FATAL: API did not become healthy within ${MAX_WAIT}s"
echo "--- systemd status ---"
systemctl status "$SERVICE_NAME" --no-pager 2>&1 || true
echo "--- journal (last 30 lines) ---"
journalctl -u "$SERVICE_NAME" --no-pager -n 30 2>&1 || true
exit 1
