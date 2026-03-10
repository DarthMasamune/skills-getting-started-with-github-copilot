"""
Tests for GET /activities endpoint
"""
import pytest


def test_get_activities_returns_200(client):
    """Test that GET /activities returns 200 OK"""
    response = client.get("/activities")
    assert response.status_code == 200


def test_get_activities_returns_dict(client):
    """Test that GET /activities returns a dictionary"""
    response = client.get("/activities")
    data = response.json()
    assert isinstance(data, dict)


def test_get_activities_contains_expected_activities(client):
    """Test that response contains expected activities"""
    response = client.get("/activities")
    data = response.json()
    
    # Verify some expected activities exist
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    for activity in expected_activities:
        assert activity in data, f"Expected activity '{activity}' not found"


def test_activity_has_required_fields(client):
    """Test that each activity has all required fields"""
    response = client.get("/activities")
    data = response.json()
    
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    for activity_name, activity_data in data.items():
        for field in required_fields:
            assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"


def test_activity_participants_is_list(client):
    """Test that participants field is a list"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        assert isinstance(activity_data["participants"], list), \
            f"Participants for '{activity_name}' is not a list"


def test_activity_max_participants_is_positive(client):
    """Test that max_participants is a positive integer"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        max_participants = activity_data["max_participants"]
        assert isinstance(max_participants, int), \
            f"max_participants for '{activity_name}' is not an integer"
        assert max_participants > 0, \
            f"max_participants for '{activity_name}' should be positive"


def test_activity_participants_count_valid(client):
    """Test that participant count doesn't exceed max_participants"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        current_count = len(activity_data["participants"])
        max_count = activity_data["max_participants"]
        assert current_count <= max_count, \
            f"Activity '{activity_name}' has {current_count} participants but max is {max_count}"
