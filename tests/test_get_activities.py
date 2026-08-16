"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """
    Test that GET /activities returns all activities with correct structure.
    """
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    
    # Verify at least some expected activities are present
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities


def test_get_activities_has_correct_structure(client):
    """
    Test that each activity has the required fields.
    """
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_get_activities_participants_are_emails(client):
    """
    Test that participants are email strings.
    """
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant


def test_get_activities_max_participants_is_positive(client):
    """
    Test that max_participants is a positive integer.
    """
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["max_participants"], int)
        assert activity_data["max_participants"] > 0


def test_get_activities_participant_count_does_not_exceed_max(client):
    """
    Test that participant count doesn't exceed max_participants.
    """
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        participant_count = len(activity_data["participants"])
        max_participants = activity_data["max_participants"]
        assert participant_count <= max_participants, \
            f"{activity_name} has {participant_count} participants but max is {max_participants}"
