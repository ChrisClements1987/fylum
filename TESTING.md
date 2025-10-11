# Fylum Testing Guide

## Overview

Fylum follows Test-Driven Development (TDD) principles with comprehensive testing for both backend and frontend.

## Test Structure

```
fylum/
├── tests/                      # Python/Backend tests
│   ├── test_config.py         # V1.0.0 config tests
│   ├── test_engine.py         # V1.0.0 engine tests
│   ├── test_processor.py      # V1.0.0 processor tests
│   ├── test_integration.py    # V1.0.0 integration tests
│   ├── test_security_edge_cases.py  # V1.0.0 security tests
│   ├── test_api_config.py     # V2.0.0 API config tests
│   ├── test_api_operations.py # V2.0.0 API operations tests
│   ├── test_api_history.py    # V2.0.0 API history tests
│   └── test_api_integration.py # V2.0.0 API integration tests
└── web/src/__tests__/          # Frontend tests
    └── App.test.js            # Svelte component tests
```

## Running Tests

### All Tests (Automated)

```bash
python run_tests.py
```

This runs both backend and frontend tests with coverage reports.

### Backend Tests Only

```bash
# All backend tests
pytest

# With coverage
pytest --cov=src tests/

# Specific test file
pytest tests/test_api_config.py -v

# Specific test
pytest tests/test_api_config.py::test_get_config_success -v

# V1.0.0 tests only
pytest tests/test_config.py tests/test_engine.py tests/test_processor.py

# V2.0.0 API tests only
pytest tests/test_api_*.py
```

### Frontend Tests Only

```bash
cd web

# Run tests
npm run test

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage

# Watch mode
npm run test -- --watch
```

## Test Categories

### Unit Tests
Test individual components in isolation.

**Backend:**
- `test_config.py` - Configuration loading and validation
- `test_engine.py` - File matching logic
- `test_processor.py` - File operations
- `test_api_config.py` - API config endpoints
- `test_api_operations.py` - API operation endpoints
- `test_api_history.py` - API history endpoints

**Frontend:**
- `App.test.js` - App component rendering and behavior

### Integration Tests
Test workflows across multiple components.

**Backend:**
- `test_integration.py` - End-to-end CLI workflows
- `test_api_integration.py` - End-to-end API workflows

### Security Tests
Test security and edge cases.

- `test_security_edge_cases.py` - Path traversal, permissions, unicode, etc.

## Writing New Tests

### Backend Test Template (pytest)

```python
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_feature_name():
    """Test description"""
    # Arrange
    test_data = {"key": "value"}
    
    # Act
    response = client.post("/api/endpoint", json=test_data)
    
    # Assert
    assert response.status_code == 200
    assert response.json()["success"] is True
```

### Frontend Test Template (Vitest)

```javascript
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/svelte';
import Component from '../Component.svelte';

describe('Component', () => {
  it('renders correctly', () => {
    render(Component);
    expect(screen.getByText('Expected Text')).toBeTruthy();
  });
});
```

## Test Coverage Goals

- **Overall Coverage**: > 80%
- **Critical Paths**: 100% (config loading, file operations, API endpoints)
- **V1.0.0 Core**: 95%+ (already achieved)
- **V2.0.0 API**: 90%+ (target)
- **V2.0.0 Frontend**: 80%+ (target)

## Continuous Integration

Tests are automatically run on:
- Every commit to `develop/*` branches
- Every pull request
- Before releases

## Test Data

Tests use temporary directories and mock data to avoid affecting real files.

**Never test on:**
- Real user directories
- Production config files
- Actual Downloads/Documents folders

## Debugging Tests

### Backend

```bash
# Run with verbose output
pytest -vv

# Show print statements
pytest -s

# Drop into debugger on failure
pytest --pdb

# Run specific test with full traceback
pytest tests/test_api_config.py::test_get_config_success -vv --tb=long
```

### Frontend

```bash
cd web

# Run with UI for debugging
npm run test:ui

# Watch mode
npm run test -- --watch

# Show console output
npm run test -- --reporter=verbose
```

## Performance Testing

### API Response Times

```bash
pytest tests/test_api_integration.py::test_api_response_times -v
```

All API endpoints should respond within 1 second.

## Common Issues

### Backend: ImportError
**Solution**: Ensure you're in the project root and venv is activated

### Backend: FastAPI tests fail
**Solution**: Install httpx: `pip install httpx`

### Frontend: Module not found
**Solution**: Run `npm install` in web/ directory

### Frontend: Tests timeout
**Solution**: Increase timeout in vite.config.js test section

## Best Practices

1. **Write tests first** (TDD)
2. **One assertion per test** (when possible)
3. **Clear test names** - describe what's being tested
4. **Arrange-Act-Assert** pattern
5. **Use fixtures** for reusable test data
6. **Mock external dependencies** (API calls, file system)
7. **Clean up** test files and state
8. **Test edge cases** and error conditions

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [Vitest documentation](https://vitest.dev/)
- [Testing Library Svelte](https://testing-library.com/docs/svelte-testing-library/intro/)
- [FastAPI testing guide](https://fastapi.tiangolo.com/tutorial/testing/)

---

**Last Updated**: October 10, 2025  
**Test Coverage**: 85% overall
