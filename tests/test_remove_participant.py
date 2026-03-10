"""
Tests for DELETE /activities/{activity_name}/participants/{email} endpoint
"""
import pytest


def test_remove_participant_success(client):
    """Test successful removal of a participant"""
    activity = "Basketball Team"
    email = "james@mergington.edu"  # Existing participant
    
    # Get initial participant count
    response = client.get("/activities")
    initial_count = len(response.json()[activity]["participants"])
    
    # Remove participant
    response = client.delete(f"/activities/{activity}/participants/{email}")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]
    
    # Verify participant was removed
    response = client.get("/activities")
    participants = response.json()[activity]["participants"]
    assert email not in participants
    assert len(participants) == initial_count - 1


def test_remove_nonexistent_participant_returns_404(client):
    """Test removing a participant that doesn't exist returns 404"""
    activity = "Gym Class"
    email = "nonexistent@mergington.edu"
    
    response = client.delete(f"/activities/{activity}/participants/{email}")
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_remove_participant_from_nonexistent_activity_returns_404(client):
    """Test removing participant from non-existent activity returns 404"""
    activity = "Nonexistent Activity"
    email = "test@mergington.edu"
    
    response = client.delete(f"/activities/{activity}/participants/{email}")
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "activity" in data["detail"].lower()


def test_remove_participant_with_url_encoding(client):
    """Test removal with URL-encoded activity name"""
    # First add a participant to Programming Class
    activity = "Programming Class"
    email = "emma@mergington.edu"  # Existing participant
    
    response = client.delete(f"/activities/{activity}/participants/{email}")
    
    # Should handle URL encoding properly
    assert response.status_code == 200


def test_remove_participant_with_special_characters_in_email(client):
    """Test removal with special characters in email"""
    # First, sign up with special characters
    activity = "Art Studio"
    email = "special+test@mergington.edu"
    
    # Sign up
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Then remove
    response = client.delete(f"/activities/{activity}/participants/{email}")
    
    assert response.status_code == 200


def test_remove_participant_updates_immediately(client):
    """Test that removal updates are reflected in GET /activities"""
    activity = "Tennis Club"
    email = "lucas@mergington.edu"  # Existing participant
    
    # Get initial state
    response = client.get("/activities")
    initial_participants = response.json()[activity]["participants"].copy()
    assert email in initial_participants
    
    # Remove participant
    client.delete(f"/activities/{activity}/participants/{email}")
    
    # Verify update
    response = client.get("/activities")
    updated_participants = response.json()[activity]["participants"]
    
    assert email not in updated_participants
    assert len(updated_participants) == len(initial_participants) - 1


def test_remove_participant_response_format(client):
    """Test that remove response has correct format"""
    activity = "Drama Club"
    email = "sarah@mergington.edu"  # Existing participant
    
    response = client.delete(f"/activities/{activity}/participants/{email}")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)


def test_remove_last_participant(client):
    """Test removing the last participant from an activity"""
    # First ensure Science Club has only one test participant
    activity = "Science Club"
    test_email = "solo.participant@mergington.edu"
    
    # Add our test participant
    client.post(f"/activities/{activity}/signup", params={"email": test_email})
    
    # Remove them
    response = client.delete(f"/activities/{activity}/participants/{test_email}")
    
    assert response.status_code == 200
    
    # Verify participants list still exists (as empty list)
    response = client.get("/activities")
    activity_data = response.json()[activity]
    assert "participants" in activity_data
    assert isinstance(activity_data["participants"], list)
