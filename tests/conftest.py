"""
Shared pytest configuration and fixtures for FastAPI backend tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provides a TestClient for making HTTP requests to the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Returns the current activities dictionary from the app.
    This allows tests to reference the app's activity data.
    """
    return activities


@pytest.fixture(autouse=True)
def reset_activities_state():
    """
    Reset the participants list after each test to ensure test isolation.
    This runs automatically before and after each test.
    """
    # Store original state
    original_state = {}
    for activity_name, activity_data in activities.items():
        original_state[activity_name] = activity_data["participants"].copy()
    
    yield
    
    # Reset to original state after test
    for activity_name, activity_data in activities.items():
        activity_data["participants"] = original_state[activity_name].copy()
