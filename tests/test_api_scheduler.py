"""
API tests for scheduler endpoints (TDD - tests first)
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from src.api.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def ensure_config():
    """Ensure config.yaml exists for tests"""
    from src.config import create_default_config
    config_path = Path("config.yaml")
    
    if not config_path.exists():
        create_default_config()
    
    yield


def test_get_all_schedules():
    """Test GET /api/scheduler/ returns all schedules"""
    response = client.get("/api/scheduler/")
    assert response.status_code == 200
    
    data = response.json()
    assert "schedules" in data
    assert isinstance(data["schedules"], list)


def test_create_schedule():
    """Test POST /api/scheduler/ creates a new schedule"""
    schedule_data = {
        "name": "Daily Clean",
        "cron_expression": "0 9 * * *",
        "enabled": True
    }
    
    response = client.post("/api/scheduler/", json=schedule_data)
    assert response.status_code in [200, 201]
    
    data = response.json()
    assert "id" in data
    assert data["name"] == "Daily Clean"


def test_get_schedule_by_id():
    """Test GET /api/scheduler/{id} returns specific schedule"""
    # Create a schedule first
    schedule_data = {
        "name": "Test Schedule",
        "cron_expression": "0 10 * * *",
        "enabled": True
    }
    
    create_response = client.post("/api/scheduler/", json=schedule_data)
    assert create_response.status_code in [200, 201]
    
    schedule_id = create_response.json()["id"]
    
    # Get the schedule
    response = client.get(f"/api/scheduler/{schedule_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == schedule_id
    assert data["name"] == "Test Schedule"


def test_update_schedule():
    """Test PUT /api/scheduler/{id} updates a schedule"""
    # Create a schedule first
    schedule_data = {
        "name": "Original Name",
        "cron_expression": "0 9 * * *",
        "enabled": True
    }
    
    create_response = client.post("/api/scheduler/", json=schedule_data)
    schedule_id = create_response.json()["id"]
    
    # Update it
    update_data = {
        "name": "Updated Name",
        "cron_expression": "0 10 * * *",
        "enabled": False
    }
    
    response = client.put(f"/api/scheduler/{schedule_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "Updated Name"


def test_delete_schedule():
    """Test DELETE /api/scheduler/{id} removes a schedule"""
    # Create a schedule first
    schedule_data = {
        "name": "To Delete",
        "cron_expression": "0 9 * * *",
        "enabled": True
    }
    
    create_response = client.post("/api/scheduler/", json=schedule_data)
    schedule_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/api/scheduler/{schedule_id}")
    assert response.status_code in [200, 204]
    
    # Verify it's gone
    get_response = client.get(f"/api/scheduler/{schedule_id}")
    assert get_response.status_code == 404


def test_enable_schedule_endpoint():
    """Test POST /api/scheduler/{id}/enable"""
    schedule_data = {
        "name": "Test Schedule",
        "cron_expression": "0 9 * * *",
        "enabled": False
    }
    
    create_response = client.post("/api/scheduler/", json=schedule_data)
    schedule_id = create_response.json()["id"]
    
    response = client.post(f"/api/scheduler/{schedule_id}/enable")
    assert response.status_code == 200
    
    # Verify it's enabled
    get_response = client.get(f"/api/scheduler/{schedule_id}")
    assert get_response.json()["enabled"] is True


def test_disable_schedule_endpoint():
    """Test POST /api/scheduler/{id}/disable"""
    schedule_data = {
        "name": "Test Schedule",
        "cron_expression": "0 9 * * *",
        "enabled": True
    }
    
    create_response = client.post("/api/scheduler/", json=schedule_data)
    schedule_id = create_response.json()["id"]
    
    response = client.post(f"/api/scheduler/{schedule_id}/disable")
    assert response.status_code == 200
    
    # Verify it's disabled
    get_response = client.get(f"/api/scheduler/{schedule_id}")
    assert get_response.json()["enabled"] is False


def test_invalid_cron_expression():
    """Test creating schedule with invalid cron expression"""
    schedule_data = {
        "name": "Invalid Schedule",
        "cron_expression": "invalid cron",
        "enabled": True
    }
    
    response = client.post("/api/scheduler/", json=schedule_data)
    # Should reject invalid cron
    assert response.status_code in [400, 422]


def test_schedule_run_history():
    """Test GET /api/scheduler/{id}/history returns execution history"""
    schedule_data = {
        "name": "Test Schedule",
        "cron_expression": "0 9 * * *",
        "enabled": True
    }
    
    create_response = client.post("/api/scheduler/", json=schedule_data)
    schedule_id = create_response.json()["id"]
    
    response = client.get(f"/api/scheduler/{schedule_id}/history")
    assert response.status_code == 200
    
    data = response.json()
    assert "runs" in data
    assert isinstance(data["runs"], list)
