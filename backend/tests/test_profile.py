"""Tests for profile endpoints"""

import pytest
from fastapi import status


class TestGetProfile:
    """Test getting user profile"""

    def test_get_profile_success(self, client, auth_headers):
        """Test getting profile with valid authentication"""
        response = client.get("/api/profile", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"

    def test_get_profile_unauthorized(self, client):
        """Test getting profile without authentication"""
        response = client.get("/api/profile")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestUpdateProfile:
    """Test updating user profile"""

    def test_update_profile_success(self, client, auth_headers):
        """Test successful profile update"""
        response = client.put(
            "/api/profile",
            headers=auth_headers,
            json={"name": "Updated Name", "age": 35, "weight_kg": 75},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["age"] == 35
        assert float(data["weight_kg"]) == 75.0

    def test_update_profile_partial(self, client, auth_headers):
        """Test partial profile update"""
        response = client.put(
            "/api/profile", headers=auth_headers, json={"name": "New Name Only"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "New Name Only"
        assert data["email"] == "test@example.com"  # Unchanged

    def test_update_profile_invalid_age(self, client, auth_headers):
        """Test profile update with invalid age"""
        response = client.put("/api/profile", headers=auth_headers, json={"age": -5})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_profile_unauthorized(self, client):
        """Test profile update without authentication"""
        response = client.put("/api/profile", json={"name": "Should Fail"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
