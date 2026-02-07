"""
Phase 23: Backend E2E API Tests

Tests that verify the API works end-to-end:
- OpenAPI schema is accessible and valid
- Health endpoint returns real status
- Full auth flow: register → login → /me
- Authenticated access to business data (nutrition summary)
"""


class TestAPISchemaE2E:
    """API schema is accessible and structurally valid."""

    def test_openapi_schema_accessible(self, e2e_client):
        """GET /openapi.json returns valid OpenAPI schema with expected paths."""
        response = e2e_client.get("/openapi.json")
        assert response.status_code == 200

        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema

        paths = schema["paths"]
        assert "/api/auth/login" in paths
        assert "/api/auth/register" in paths
        assert "/api/nutrition/food-log" in paths

    def test_docs_endpoint_accessible(self, e2e_client):
        """GET /docs returns Swagger UI page."""
        response = e2e_client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()


class TestHealthEndpointE2E:
    """Health check returns real status data."""

    def test_health_returns_healthy(self, e2e_client):
        """GET /health returns {"status": "healthy"}."""
        response = e2e_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_root_returns_app_info(self, e2e_client):
        """GET / returns app name, version, and online status."""
        response = e2e_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["status"] == "online"


class TestAuthFlowE2E:
    """Full authentication flow: register → login → access protected resource."""

    def test_full_auth_flow(self, e2e_client):
        """Register, login, and access /me — complete E2E auth flow."""
        # Step 1: Register
        reg_response = e2e_client.post("/api/auth/register", json={
            "email": "e2e-test@example.com",
            "password": "e2e-password-123",
            "name": "E2E Test User",
        })
        assert reg_response.status_code == 201
        user_data = reg_response.json()
        assert user_data["email"] == "e2e-test@example.com"
        assert "id" in user_data
        assert "password_hash" not in user_data

        # Step 2: Login (OAuth2 form format)
        login_response = e2e_client.post("/api/auth/login", data={
            "username": "e2e-test@example.com",
            "password": "e2e-password-123",
        })
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"

        # Step 3: Access /me with token
        me_response = e2e_client.get("/api/auth/me", headers={
            "Authorization": f"Bearer {token_data['access_token']}"
        })
        assert me_response.status_code == 200
        me_data = me_response.json()
        assert me_data["email"] == "e2e-test@example.com"
        assert me_data["name"] == "E2E Test User"

    def test_login_token_accesses_business_data(self, e2e_client):
        """Login token can access nutrition daily summary (business data)."""
        # Register + login
        e2e_client.post("/api/auth/register", json={
            "email": "e2e-biz@example.com",
            "password": "e2e-password-123",
            "name": "E2E Biz User",
        })
        login_resp = e2e_client.post("/api/auth/login", data={
            "username": "e2e-biz@example.com",
            "password": "e2e-password-123",
        })
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Access nutrition daily summary (valid schema even if empty)
        summary_resp = e2e_client.get("/api/nutrition/daily-summary", headers=headers)
        assert summary_resp.status_code == 200
        data = summary_resp.json()
        assert "total_calories" in data
        assert "entries_count" in data
