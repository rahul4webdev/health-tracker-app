# API 503 Root Cause Diagnosis

## Symptom
`https://healthapi.gahfaudio.in/health` returns HTTP 503 (LiteSpeed "temporarily busy").

## Server Environment
- **Hosting server**: `62.72.58.74` (CyberPanel / LiteSpeed)
- **NOT** on the AI platform VPS (`82.25.110.109`)
- **Deployment**: GitHub Actions rsync via SSH
- **Backend path**: `/home/healthapi.gahfaudio.in/public_html/`
- **Expected port**: 8022 (uvicorn)

## Root Cause (confirmed)

### 1. Backend process never starts after deployment
The workflow file `deploy-testing.yml` line 158:
```bash
sudo systemctl restart health-tracker-api || echo "Service restart skipped (configure systemd first)"
```
The `health-tracker-api` systemd service **does not exist** on the CyberPanel hosting server.
The `|| echo` suppresses the error, so the workflow reports success while the API process is never started.

### 2. Smoke tests silently pass
Lines 228-240 use `|| echo "WARNING:..."` which always exits 0.
A 503 response from the health check does NOT fail the workflow.

### 3. No process management
There is no `start_server.sh` script. The alternative uvicorn start command is commented out.
After code is rsynced, nothing actually starts the FastAPI application.

### 4. LiteSpeed proxy returns 503
LiteSpeed is configured to proxy to `127.0.0.1:8022`, but since uvicorn is not running,
the connection is refused and LiteSpeed returns 503.

## Fix Applied
1. Created `backend/scripts/start_server.sh` — kills old process, starts uvicorn on port 8022
2. Updated workflow to use `start_server.sh` + verify with `curl -f`
3. Made smoke tests fail-hard (removed `|| echo` fallback)
4. Added `.env` recreation on every deploy (was only created if missing)
5. Added `backend/tests/e2e/test_health_startup.py` for local verification
