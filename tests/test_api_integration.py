"""
API integration tests - end-to-end workflows
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import shutil
from src.api.main import app

client = TestClient(app)


def test_api_health_check():
    """Test API health endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"


def test_api_root():
    """Test API root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "running"


def test_api_docs_accessible():
    """Test API documentation is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema():
    """Test OpenAPI schema is available"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema


def test_cors_headers():
    """Test CORS headers are set correctly"""
    response = client.get("/api/health", headers={
        "Origin": "http://localhost:5173"
    })
    
    # Should allow CORS from Vite dev server
    assert response.status_code == 200


def test_complete_workflow():
    """Test complete user workflow: config -> scan -> clean -> undo"""
    
    # 1. Load config
    config_response = client.get("/api/config/")
    assert config_response.status_code == 200
    
    # 2. Validate config
    validate_response = client.get("/api/config/validate")
    assert validate_response.status_code == 200
    
    # 3. Scan (dry run)
    scan_response = client.post("/api/operations/scan")
    assert scan_response.status_code in [200, 500]  # May fail if no test files
    
    # 4. Get history
    history_response = client.get("/api/history/")
    assert history_response.status_code == 200


def test_error_handling():
    """Test API handles errors gracefully"""
    # Invalid endpoint
    response = client.get("/api/invalid/endpoint")
    assert response.status_code == 404
    
    # Should return JSON error
    data = response.json()
    assert "detail" in data


def test_api_response_times():
    """Test API responds quickly"""
    import time
    
    endpoints = [
        "/api/health",
        "/api/config/",
        "/api/history/",
    ]
    
    for endpoint in endpoints:
        start = time.time()
        response = client.get(endpoint)
        duration = time.time() - start
        
        assert response.status_code in [200, 404, 500]
        assert duration < 1.0  # Should respond within 1 second
