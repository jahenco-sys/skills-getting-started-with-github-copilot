def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    body = response.json()
    assert response.status_code == 200
    assert expected_activity_name in body
    assert "participants" in body[expected_activity_name]


def test_signup_success_returns_message_and_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    activity_name_path = "Chess%20Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name_path}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    activity_name_path = "Chess%20Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name_path}/signup?email={existing_email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    unknown_activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{unknown_activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_success_returns_message_and_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    activity_name_path = "Chess%20Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name_path}/signup?email={existing_email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {existing_email} from {activity_name}"
    activities_response = client.get("/activities")
    assert existing_email not in activities_response.json()[activity_name]["participants"]


def test_unregister_non_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    activity_name_path = "Chess%20Club"
    absent_email = "notsignedup@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name_path}/signup?email={absent_email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    unknown_activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{unknown_activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
