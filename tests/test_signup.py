"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_successful(client):
    """
    Test successful signup: new participant is added and returns 200.
    """
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant_to_activity(client):
    """
    Test that signup actually adds the participant to the activity.
    """
    new_email = "test@mergington.edu"
    
    # Get initial state
    response1 = client.get("/activities")
    activities1 = response1.json()
    initial_participants = activities1["Chess Club"]["participants"].copy()
    
    # Sign up
    client.post(
        "/activities/Chess Club/signup",
        params={"email": new_email}
    )
    
    # Verify participant added
    response2 = client.get("/activities")
    activities2 = response2.json()
    final_participants = activities2["Chess Club"]["participants"]
    
    assert new_email in final_participants
    assert len(final_participants) == len(initial_participants) + 1


def test_signup_duplicate_returns_400(client):
    """
    Test that signing up with a duplicate email returns 400 error.
    """
    # First signup should succeed
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": "duplicate@mergington.edu"}
    )
    assert response1.status_code == 200
    
    # Second signup with same email should fail
    response2 = client.post(
        "/activities/Chess Club/signup",
        params={"email": "duplicate@mergington.edu"}
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity_returns_404(client):
    """
    Test that signup to a nonexistent activity returns 404 error.
    """
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


@pytest.mark.parametrize("activity_name", [
    "Chess Club",
    "Programming Class",
    "Gym Class",
    "Basketball Team",
    "Tennis Club"
])
def test_signup_multiple_activities(client, activity_name):
    """
    Test signup works for multiple different activities.
    """
    email = f"student_{activity_name.replace(' ', '_')}@mergington.edu"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    
    # Verify in activity list
    response2 = client.get("/activities")
    activities = response2.json()
    assert email in activities[activity_name]["participants"]


def test_signup_response_format(client):
    """
    Test that signup response has expected format.
    """
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "format_test@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)


def test_signup_user_can_signup_for_multiple_activities(client):
    """
    Test that the same user can sign up for multiple different activities.
    """
    email = "multi_activity@mergington.edu"
    
    # Sign up for Chess Club
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up for Programming Class (same email, different activity)
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify in both activities
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]
