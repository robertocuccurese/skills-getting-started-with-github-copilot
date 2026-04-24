from urllib.parse import quote

from src.app import activities


def test_unregister_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_activity_not_found(client):
    # Arrange
    activity_name = "Unknown Activity"
    endpoint = f"/activities/{quote(activity_name)}/participants"

    # Act
    response = client.delete(endpoint, params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_not_found(client):
    # Arrange
    activity_name = "Chess Club"
    endpoint = f"/activities/{quote(activity_name)}/participants"

    # Act
    response = client.delete(endpoint, params={"email": "missing@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
