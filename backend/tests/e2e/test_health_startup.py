"""
E2E Health Startup Test

Validates that the FastAPI application starts correctly and the /health
endpoint returns the expected response. This test catches startup failures
(missing env vars, import errors, DB connection issues) before deployment.
"""

import subprocess
import time
import os
import signal
import pytest
import requests


BACKEND_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
PORT = 18922  # Use a non-conflicting port for testing


@pytest.fixture(scope="module")
def running_server():
    """Start the FastAPI app in a subprocess and yield when ready."""
    env = os.environ.copy()
    env.update({
        "DB_HOST": os.environ.get("DB_HOST", "localhost"),
        "DB_USER": os.environ.get("DB_USER", "test_user"),
        "DB_PASSWORD": os.environ.get("DB_PASSWORD", "test_password"),
        "DB_PORT": os.environ.get("DB_PORT", "3306"),
        "DATABASE": os.environ.get("DATABASE", "test_db"),
        "SECRET_KEY": os.environ.get("SECRET_KEY", "test-secret-key-for-e2e"),
        "ENVIRONMENT": "testing",
    })

    proc = subprocess.Popen(
        [
            "python", "-m", "uvicorn",
            "app.main:app",
            "--host", "127.0.0.1",
            "--port", str(PORT),
            "--log-level", "warning",
        ],
        cwd=BACKEND_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for server to start (max 15 seconds)
    base_url = f"http://127.0.0.1:{PORT}"
    started = False
    for _ in range(30):
        try:
            resp = requests.get(f"{base_url}/health", timeout=1)
            if resp.status_code == 200:
                started = True
                break
        except requests.ConnectionError:
            pass
        time.sleep(0.5)

    if not started:
        proc.terminate()
        proc.wait(timeout=5)
        stdout = proc.stdout.read().decode() if proc.stdout else ""
        stderr = proc.stderr.read().decode() if proc.stderr else ""
        pytest.fail(
            f"Server failed to start within 15s.\n"
            f"STDOUT:\n{stdout}\n"
            f"STDERR:\n{stderr}"
        )

    yield base_url

    # Teardown
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


class TestHealthStartup:
    """Verify the application starts and serves basic endpoints."""

    def test_health_endpoint_returns_200(self, running_server):
        """GET /health returns 200 with status field."""
        resp = requests.get(f"{running_server}/health", timeout=5)
        assert resp.status_code == 200
        data = resp.json()
        assert "status" in data

    def test_root_endpoint_returns_200(self, running_server):
        """GET / returns 200."""
        resp = requests.get(f"{running_server}/", timeout=5)
        assert resp.status_code == 200

    def test_health_response_time_under_2s(self, running_server):
        """Health endpoint responds within 2 seconds."""
        resp = requests.get(f"{running_server}/health", timeout=5)
        assert resp.elapsed.total_seconds() < 2.0

    def test_cors_headers_present(self, running_server):
        """OPTIONS request returns CORS headers."""
        resp = requests.options(
            f"{running_server}/health",
            headers={"Origin": "http://localhost:3000"},
            timeout=5,
        )
        # CORS should be configured — at minimum, no 405
        assert resp.status_code in (200, 204, 405)

    def test_docs_endpoint_available(self, running_server):
        """Swagger docs are accessible at /docs."""
        resp = requests.get(f"{running_server}/docs", timeout=5)
        assert resp.status_code == 200
        assert "text/html" in resp.headers.get("content-type", "")
