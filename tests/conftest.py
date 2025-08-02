"""
Pytest configuration and fixtures for getter service tests
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test"""
    # Set test environment variables
    os.environ["REDIS_HOST"] = "localhost"
    os.environ["REDIS_PORT"] = "6379"
    os.environ["API_KEY_MERCADO_PUBLICO"] = "test_token"

    yield

    # Cleanup after test
    pass


@pytest.fixture
def mock_redis():
    """Mock Redis connection"""
    with patch("app.redis.Redis") as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_requests():
    """Mock requests module"""
    with patch("app.requests.get") as mock:
        yield mock


@pytest.fixture
def sample_tenders_response():
    """Sample tenders list response"""
    return {
        "Listado": [
            {"CodigoExterno": "123"},
            {"CodigoExterno": "456"},
            {"CodigoExterno": "789"},
            {"CodigoExterno": "012"},
            {"CodigoExterno": "345"},
        ]
    }


@pytest.fixture
def sample_tender_response():
    """Sample individual tender response"""
    return {
        "Listado": [
            {
                "CodigoExterno": "123",
                "Nombre": "Test Tender",
                "Descripcion": "Test Description",
            }
        ]
    }


@pytest.fixture
def expected_message():
    """Expected message structure"""
    return {
        "id": 0,
        "status": "pre-processed",
        "payload": {
            "code": "123",
            "title": "Test Tender",
            "description": "Test Description",
        },
    }
