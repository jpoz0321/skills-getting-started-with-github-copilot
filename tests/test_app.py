import pytest


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert expected_activity in activities
    assert "description" in activities[expected_activity]
    assert "participants" in activities[expected_activity]


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Gym Class"
    new_email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
    assert new_email in client.get("/activities").json()[activity_name]["participants"]


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Programming Class"
    existing_email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={existing_email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_fails_when_activity_is_full(client):
    # Arrange
    activity_name = "Math Olympiad"
    # Fill activity to max participants
    max_participants = client.get("/activities").json()[activity_name]["max_participants"]
    for i in range(max_participants - len(client.get("/activities").json()[activity_name]["participants"])):
        client.post(f"/activities/{activity_name}/signup?email=test{i}@mergington.edu")

    new_email = "overflow@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is at maximum capacity"


def test_delete_participant_removes_student(client):
    # Arrange
    activity_name = "Debate Team"
    existing_email = "oliver@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={existing_email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {existing_email} from {activity_name}"
    assert existing_email not in client.get("/activities").json()[activity_name]["participants"]


def test_delete_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Art Club"
    missing_email = "missing@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={missing_email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
