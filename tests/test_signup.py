from urllib.parse import quote

from src.app import activities


def test_signup_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_signup_activity_not_found(client):
    # Arrange
    activity_name = "Non Existing Activity"
    endpoint = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(endpoint, params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email_returns_error(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_activity_full_returns_error(client):
    # Arrange
    activity_name = "Limited Activity"
    activities[activity_name] = {
        "description": "Temporary test activity",
        "schedule": "Fridays",
        "max_participants": 1,
        "participants": ["filled@mergington.edu"],
    }
    endpoint = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(endpoint, params={"email": "new@mergington.edu"})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
