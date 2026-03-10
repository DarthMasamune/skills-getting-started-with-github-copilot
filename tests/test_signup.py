"""
Tests for POST /activities/{activity_name}/signup endpoint
"""
import pytest


def test_signup_success(client, test_email):
    """Test successful signup for an activity"""
    activity = "Robotics Team"
    
    # First, get current participant count
    response = client.get("/activities")
    initial_count = len(response.json()[activity]["participants"])
    
    # Sign up
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": test_email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert test_email in data["message"]
    assert activity in data["message"]
    
    # Verify participant was added
    response = client.get("/activities")
    participants = response.json()[activity]["participants"]
    assert test_email in participants
    assert len(participants) == initial_count + 1


def test_signup_duplicate_returns_400(client):
    """Test that signing up twice returns 400 Bad Request"""
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity_returns_404(client, test_email):
    """Test that signing up for non-existent activity returns 404"""
    activity = "Nonexistent Activity"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": test_email}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_with_url_encoded_activity_name(client):
    """Test signup with URL-encoded activity name (spaces)"""
    activity = "Art Studio"
    email = "new.student@mergington.edu"
    
    # URL encode the activity name
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200


def test_signup_with_special_characters_in_email(client):
    """Test signup with special characters in email"""
    activity = "Science Club"
    email = "test+special@mergington.edu"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert email in data["message"]


def test_signup_response_format(client):
    """Test that signup response has correct format"""
    activity = "Drama Club"
    email = "format.test@mergington.edu"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)


def test_signup_updates_activity_list_immediately(client):
    """Test that signup updates are reflected in GET /activities"""
    activity = "Tennis Club"
    email = "immediate.test@mergington.edu"
    
    # Get initial state
    response = client.get("/activities")
    initial_participants = response.json()[activity]["participants"].copy()
    
    # Sign up
    client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Verify update
    response = client.get("/activities")
    updated_participants = response.json()[activity]["participants"]
    
    assert email in updated_participants
    assert len(updated_participants) == len(initial_participants) + 1
