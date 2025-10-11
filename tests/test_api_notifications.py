"""
API tests for notification endpoints (TDD - tests first)
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


def test_send_notification():
    """Test POST /api/notifications/send"""
    notification_data = {
        "title": "Test Notification",
        "message": "This is a test",
        "notification_type": "info"
    }
    
    response = client.post("/api/notifications/send", json=notification_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "sent" in data
    assert isinstance(data["sent"], bool)


def test_get_notification_preferences():
    """Test GET /api/notifications/preferences"""
    response = client.get("/api/notifications/preferences")
    assert response.status_code == 200
    
    data = response.json()
    assert "enabled" in data
    assert isinstance(data["enabled"], bool)


def test_update_notification_preferences():
    """Test POST /api/notifications/preferences"""
    prefs = {"enabled": False}
    
    response = client.post("/api/notifications/preferences", json=prefs)
    assert response.status_code == 200
    
    # Verify it was updated
    get_response = client.get("/api/notifications/preferences")
    assert get_response.json()["enabled"] is False


def test_get_notification_history():
    """Test GET /api/notifications/history"""
    response = client.get("/api/notifications/history")
    assert response.status_code == 200
    
    data = response.json()
    assert "notifications" in data
    assert isinstance(data["notifications"], list)


def test_clear_notification_history():
    """Test DELETE /api/notifications/history"""
    # Send a notification first
    client.post("/api/notifications/send", json={
        "title": "Test",
        "message": "Test message",
        "notification_type": "info"
    })
    
    # Clear history
    response = client.delete("/api/notifications/history")
    assert response.status_code in [200, 204]
    
    # Verify history is empty
    get_response = client.get("/api/notifications/history")
    data = get_response.json()
    assert len(data["notifications"]) == 0


def test_test_notification():
    """Test POST /api/notifications/test sends a test notification"""
    response = client.post("/api/notifications/test")
    assert response.status_code == 200
    
    data = response.json()
    assert "sent" in data


def test_notification_availability():
    """Test GET /api/notifications/available checks if notifications work"""
    response = client.get("/api/notifications/available")
    assert response.status_code == 200
    
    data = response.json()
    assert "available" in data
    assert isinstance(data["available"], bool)
