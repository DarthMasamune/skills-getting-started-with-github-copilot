"""
Pytest configuration and shared fixtures for API tests
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture(scope="module")
def client():
    """
    Create a TestClient instance for making API requests
    Scope: module - reused across all tests in a test module
    """
    return TestClient(app)


@pytest.fixture
def test_email():
    """
    Provides a fresh test email for each test
    """
    return "test.student@mergington.edu"


@pytest.fixture
def activity_name():
    """
    Provides the default activity name for testing
    """
    return "Chess Club"
