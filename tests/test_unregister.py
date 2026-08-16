"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.
"""

import pytest


def test_unregister_successful(client):
    """
    Test successful unregister: participant is removed and returns 200.
    """
    # First, sign up
    email = "student_to_remove@mergington.edu"
    client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    
    # Then, unregister
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"] or "unregistered" in data["message"].lower()


def test_unregister_removes_participant(client):
    """
    Test that unregister actually removes the participant from the activity.
    """
    email = "participant_to_remove@mergington.edu"
    
    # Sign up
    client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    
    # Verify participant was added
    response1 = client.get("/activities")
    assert email in response1.json()["Chess Club"]["participants"]
    
    # Unregister
    client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    
    # Verify participant was removed
    response2 = client.get("/activities")
    assert email not in response2.json()["Chess Club"]["participants"]


def test_unregister_nonexistent_participant_returns_404(client):
    """
    Test that unregistering a participant who is not signed up returns 404.
    """
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "never_signed_up@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower() or "not found" in data["detail"].lower()


def test_unregister_nonexistent_activity_returns_404(client):
    """
    Test that unregistering from a nonexistent activity returns 404.
    """
    response = client.delete(
        "/activities/Nonexistent Activity/unregister",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_from_multiple_activities(client):
    """
    Test that a user can unregister from one activity while remaining in another.
    """
    email = "multi_activity_remove@mergington.edu"
    
    # Sign up for two activities
    client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )
    
    # Unregister from Chess Club
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify removed from Chess Club but still in Programming Class
    response_activities = client.get("/activities")
    activities = response_activities.json()
    assert email not in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]


def test_unregister_response_format(client):
    """
    Test that unregister response has expected format.
    """
    email = "format_check@mergington.edu"
    
    # Sign up first
    client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    
    # Unregister
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)


@pytest.mark.parametrize("activity_name", [
    "Chess Club",
    "Programming Class",
    "Gym Class"
])
def test_unregister_multiple_activities(client, activity_name):
    """
    Test unregister works for multiple different activities.
    """
    email = f"unregister_{activity_name.replace(' ', '_')}@mergington.edu"
    
    # Sign up
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Unregister
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    
    # Verify removed
    response_activities = client.get("/activities")
    activities = response_activities.json()
    assert email not in activities[activity_name]["participants"]


def test_cannot_unregister_twice(client):
    """
    Test that unregistering the same participant twice returns error on second attempt.
    """
    email = "double_unregister@mergington.edu"
    
    # Sign up
    client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    
    # First unregister should succeed
    response1 = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Second unregister should fail
    response2 = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response2.status_code == 404
