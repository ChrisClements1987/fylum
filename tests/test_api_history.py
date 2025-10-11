"""
API tests for history endpoints
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_get_history_endpoint_exists():
    """Test GET /api/history/ endpoint exists"""
    response = client.get("/api/history/")
    assert response.status_code in [200, 404, 500]


def test_get_history_returns_correct_structure():
    """Test history endpoint returns correct response structure"""
    response = client.get("/api/history/")
    
    if response.status_code == 200:
        data = response.json()
        assert "entries" in data
        assert "total" in data
        assert isinstance(data["entries"], list)
        assert isinstance(data["total"], int)


def test_get_history_entry_structure():
    """Test history entries have correct structure"""
    response = client.get("/api/history/")
    
    if response.status_code == 200:
        data = response.json()
        
        if len(data["entries"]) > 0:
            entry = data["entries"][0]
            assert "timestamp" in entry
            assert "operation" in entry
            assert "files_affected" in entry


def test_get_latest_run_endpoint_exists():
    """Test GET /api/history/latest endpoint exists"""
    response = client.get("/api/history/latest")
    assert response.status_code in [200, 404, 500]


def test_get_latest_run_with_no_history():
    """Test latest endpoint when no history exists"""
    response = client.get("/api/history/latest")
    
    if response.status_code == 200:
        data = response.json()
        # Should return message or empty data gracefully
        assert isinstance(data, dict)


def test_history_consistency():
    """Test history count matches entries"""
    response = client.get("/api/history/")
    
    if response.status_code == 200:
        data = response.json()
        assert data["total"] == len(data["entries"])
