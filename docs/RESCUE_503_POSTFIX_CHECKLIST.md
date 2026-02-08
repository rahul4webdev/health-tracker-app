# Rescue 503 — Post-Fix Checklist

## Root Cause
The API returned HTTP 503 because LiteSpeed was proxying to `127.0.0.1:8022` but no uvicorn process was listening. The deployment workflow used `systemctl restart health-tracker-api` which silently failed (the systemd service doesn't exist on the CyberPanel server). Smoke tests also silently passed due to `|| echo "WARNING:..."` fallback.

## Changes Made

### 1. `backend/scripts/start_server.sh` (NEW)
- Kills any existing uvicorn process on port 8022
- Starts uvicorn in background with nohup
- Logs to `/home/healthapi.gahfaudio.in/public_html/api.log`

### 2. `.github/workflows/deploy-testing.yml` (REWRITTEN)
- Deploy package now includes `scripts/start_server.sh`
- rsync excludes `venv`, `.env`, `api.log` (prevents wiping runtime state)
- `.env` is recreated on every deploy from GitHub Secrets (not just if missing)
- Replaced broken `systemctl restart` with `start_server.sh` + `curl -f` verification
- Smoke tests now hard-fail on non-200 responses (removed `|| echo` fallback)
- Added detailed failure diagnostics (log tail, process list) on startup failure

### 3. `backend/litespeed_proxy.conf.template` (NEW)
- Documents CyberPanel/LiteSpeed external app + context configuration
- Troubleshooting steps for 503 errors

### 4. `backend/tests/e2e/test_health_startup.py` (NEW)
- Starts FastAPI app in subprocess, validates /health, /, /docs endpoints
- Catches startup failures before deployment

### 5. `controller/micro_remediator.py` (MODIFIED)
- Added `HTTP_503` failure pattern for service-not-running scenarios
- Added classification: 503 in message → HTTP_503 + INFRA owner
- Added remediation strategy: verify process, check start script, review logs

## Verification Checklist

- [ ] Trigger GitHub Actions `Deploy to Testing Environment` workflow
- [ ] Verify workflow completes without errors
- [ ] Verify `curl https://healthapi.gahfaudio.in/health` returns 200
- [ ] Verify `curl https://health.gahfaudio.in/` returns 200
- [ ] Verify smoke tests in workflow pass (no silent fallbacks)
- [ ] Check that E2E tests run after smoke tests

## Prevention

1. **No silent failures**: All deployment steps now hard-fail on error
2. **Process verification**: Workflow verifies uvicorn is running after start
3. **E2E health test**: Catches startup issues in CI before deploy
4. **503 micro-remediation**: Platform auto-detects and creates fix tasks for 503 errors
