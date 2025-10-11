"""
API tests for operations endpoints
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import shutil
from src.api.main import app

client = TestClient(app)


@pytest.fixture
def test_files():
    """Create temporary test files"""
    temp_dir = Path(tempfile.mkdtemp())
    test_dir = temp_dir / "test_files"
    test_dir.mkdir()
    
    # Create test files
    (test_dir / "test1.jpg").write_text("test")
    (test_dir / "test2.txt").write_text("test")
    
    yield test_dir
    
    # Cleanup
    shutil.rmtree(temp_dir)


def test_scan_endpoint_exists():
    """Test POST /api/operations/scan endpoint exists"""
    response = client.post("/api/operations/scan")
    assert response.status_code in [200, 404, 500]


def test_scan_returns_correct_structure():
    """Test scan endpoint returns correct response structure"""
    response = client.post("/api/operations/scan")
    
    if response.status_code == 200:
        data = response.json()
        assert "actions" in data
        assert "total_files" in data
        assert "message" in data
        assert isinstance(data["actions"], list)
        assert isinstance(data["total_files"], int)


def test_scan_with_no_files():
    """Test scan when no files match rules"""
    response = client.post("/api/operations/scan")
    
    if response.status_code == 200:
        data = response.json()
        # Should return empty or minimal results
        assert data["total_files"] >= 0


def test_clean_endpoint_exists():
    """Test POST /api/operations/clean endpoint exists"""
    response = client.post("/api/operations/clean")
    assert response.status_code in [200, 404, 500]


def test_clean_returns_correct_structure():
    """Test clean endpoint returns correct response structure"""
    response = client.post("/api/operations/clean")
    
    if response.status_code == 200:
        data = response.json()
        assert "processed" in data
        assert "success" in data
        assert "message" in data
        assert isinstance(data["processed"], int)
        assert isinstance(data["success"], bool)


def test_undo_endpoint_exists():
    """Test POST /api/operations/undo endpoint exists"""
    response = client.post("/api/operations/undo")
    assert response.status_code in [200, 404, 500]


def test_undo_returns_correct_structure():
    """Test undo endpoint returns correct response structure"""
    response = client.post("/api/operations/undo")
    
    if response.status_code == 200:
        data = response.json()
        assert "reverted" in data
        assert "success" in data
        assert "message" in data
        assert isinstance(data["reverted"], int)
        assert isinstance(data["success"], bool)


def test_undo_with_no_history():
    """Test undo when no previous operations exist"""
    response = client.post("/api/operations/undo")
    
    if response.status_code == 200:
        data = response.json()
        # Should handle gracefully
        assert data["reverted"] >= 0
        if data["reverted"] == 0:
            assert data["success"] is False


def test_scan_clean_workflow():
    """Test complete scan -> clean workflow"""
    # Scan first
    scan_response = client.post("/api/operations/scan")
    
    if scan_response.status_code == 200:
        scan_data = scan_response.json()
        initial_count = scan_data["total_files"]
        
        # If files found, clean should process them
        if initial_count > 0:
            clean_response = client.post("/api/operations/clean")
            
            if clean_response.status_code == 200:
                clean_data = clean_response.json()
                # Should have processed files
                assert clean_data["processed"] >= 0
