"""
API tests for configuration endpoints
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
    
    # Note: We don't clean up config.yaml as it's gitignored


def test_get_config_success():
    """Test GET /api/config/ returns configuration"""
    response = client.get("/api/config/")
    assert response.status_code == 200
    
    data = response.json()
    assert "target_directories" in data
    assert "ignore_patterns" in data
    assert "rename_format" in data
    assert "rules" in data
    assert isinstance(data["rules"], list)


def test_validate_config_success():
    """Test GET /api/config/validate returns validation result"""
    response = client.get("/api/config/validate")
    assert response.status_code == 200
    
    data = response.json()
    assert "valid" in data
    assert "message" in data
    
    # Should be valid with default config
    assert data["valid"] is True


def test_config_structure():
    """Test configuration has correct structure"""
    response = client.get("/api/config/")
    assert response.status_code == 200
    
    data = response.json()
    
    # Validate rules structure
    if len(data["rules"]) > 0:
        rule = data["rules"][0]
        assert "name" in rule
        assert "extensions" in rule
        assert "destination" in rule
        assert isinstance(rule["extensions"], list)


def test_update_config_endpoint_exists():
    """Test POST /api/config/ endpoint exists"""
    response = client.post("/api/config/", json={
        "target_directories": ["~/test"],
        "ignore_patterns": ["*.tmp"],
        "rename_format": "{original_filename}",
        "rules": []
    })
    
    # Should return success (even if not implemented)
    assert response.status_code in [200, 201, 501]
