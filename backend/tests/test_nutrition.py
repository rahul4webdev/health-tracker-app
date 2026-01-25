"""Tests for nutrition endpoints"""

import pytest
from datetime import datetime, date
from fastapi import status


class TestCreateFoodLog:
    """Test creating food log entries"""

    def test_create_food_log_success(self, client, auth_headers):
        """Test successful food log creation"""
        response = client.post(
            "/api/nutrition/food-log",
            headers=auth_headers,
            json={
                "food_name": "Apple",
                "calories": 95.5,
                "protein_g": 0.5,
                "carbs_g": 25.0,
                "fats_g": 0.3,
                "logged_at": "2026-01-25T12:00:00",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["food_name"] == "Apple"
        assert float(data["calories"]) == 95.5

    def test_create_food_log_minimal(self, client, auth_headers):
        """Test food log creation with minimal data"""
        response = client.post(
            "/api/nutrition/food-log",
            headers=auth_headers,
            json={
                "food_name": "Banana",
                "calories": 105,
                "logged_at": "2026-01-25T14:00:00",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_food_log_invalid_calories(self, client, auth_headers):
        """Test food log creation with negative calories"""
        response = client.post(
            "/api/nutrition/food-log",
            headers=auth_headers,
            json={
                "food_name": "Invalid",
                "calories": -10,
                "logged_at": "2026-01-25T12:00:00",
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetFoodLogs:
    """Test retrieving food logs"""

    def test_get_food_logs_empty(self, client, auth_headers):
        """Test getting food logs when none exist"""
        response = client.get("/api/nutrition/food-log", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_get_food_logs(self, client, auth_headers):
        """Test getting food logs after creating some"""
        # Create food logs
        client.post(
            "/api/nutrition/food-log",
            headers=auth_headers,
            json={
                "food_name": "Apple",
                "calories": 95,
                "logged_at": "2026-01-25T12:00:00",
            },
        )
        client.post(
            "/api/nutrition/food-log",
            headers=auth_headers,
            json={
                "food_name": "Banana",
                "calories": 105,
                "logged_at": "2026-01-25T13:00:00",
            },
        )

        # Get food logs
        response = client.get("/api/nutrition/food-log", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2


class TestGetFoodLog:
    """Test getting a specific food log"""

    def test_get_food_log_success(self, client, auth_headers):
        """Test getting a specific food log by ID"""
        # Create food log
        create_response = client.post(
            "/api/nutrition/food-log",
            headers=auth_headers,
            json={
                "food_name": "Apple",
                "calories": 95,
                "logged_at": "2026-01-25T12:00:00",
            },
        )
        food_log_id = create_response.json()["id"]

        # Get food log
        response = client.get(
            f"/api/nutrition/food-log/{food_log_id}", headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["food_name"] == "Apple"

    def test_get_food_log_not_found(self, client, auth_headers):
        """Test getting nonexistent food log"""
        response = client.get("/api/nutrition/food-log/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateFoodLog:
    """Test updating food log entries"""

    def test_update_food_log_success(self, client, auth_headers):
        """Test successful food log update"""
        # Create food log
        create_response = client.post(
            "/api/nutrition/food-log",
            headers=auth_headers,
            json={
                "food_name": "Apple",
                "calories": 95,
                "logged_at": "2026-01-25T12:00:00",
            },
        )
        food_log_id = create_response.json()["id"]

        # Update food log
        response = client.put(
            f"/api/nutrition/food-log/{food_log_id}",
            headers=auth_headers,
            json={"food_name": "Green Apple", "calories": 100},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["food_name"] == "Green Apple"
        assert float(data["calories"]) == 100


class TestDeleteFoodLog:
    """Test deleting food log entries"""

    def test_delete_food_log_success(self, client, auth_headers):
        """Test successful food log deletion"""
        # Create food log
        create_response = client.post(
            "/api/nutrition/food-log",
            headers=auth_headers,
            json={
                "food_name": "Apple",
                "calories": 95,
                "logged_at": "2026-01-25T12:00:00",
            },
        )
        food_log_id = create_response.json()["id"]

        # Delete food log
        response = client.delete(
            f"/api/nutrition/food-log/{food_log_id}", headers=auth_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify deletion
        get_response = client.get(
            f"/api/nutrition/food-log/{food_log_id}", headers=auth_headers
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


class TestDailySummary:
    """Test daily nutrition summary"""

    def test_daily_summary_empty(self, client, auth_headers):
        """Test daily summary with no entries"""
        response = client.get(
            "/api/nutrition/daily-summary?date=2026-01-25", headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["date"] == "2026-01-25"
        assert float(data["total_calories"]) == 0
        assert data["entries_count"] == 0

    def test_daily_summary_with_entries(self, client, auth_headers):
        """Test daily summary with food entries"""
        # Create food logs
        client.post(
            "/api/nutrition/food-log",
            headers=auth_headers,
            json={
                "food_name": "Apple",
                "calories": 95,
                "protein_g": 0.5,
                "carbs_g": 25,
                "fats_g": 0.3,
                "logged_at": "2026-01-25T12:00:00",
            },
        )
        client.post(
            "/api/nutrition/food-log",
            headers=auth_headers,
            json={
                "food_name": "Banana",
                "calories": 105,
                "protein_g": 1.3,
                "carbs_g": 27,
                "fats_g": 0.4,
                "logged_at": "2026-01-25T14:00:00",
            },
        )

        # Get daily summary
        response = client.get(
            "/api/nutrition/daily-summary?date=2026-01-25", headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["date"] == "2026-01-25"
        assert float(data["total_calories"]) == 200
        assert float(data["total_protein_g"]) == 1.8
        assert data["entries_count"] == 2
