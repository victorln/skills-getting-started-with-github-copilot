import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert: Test listing activities
def test_list_activities():
    # Arrange: (nothing to arrange for this test)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Arrange-Act-Assert: Test successful signup
def test_signup_success():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Cleanup
    client.delete(f"/activities/{activity}/unregister", params={"email": email})

# Arrange-Act-Assert: Test duplicate signup prevention
def test_signup_duplicate():
    # Arrange
    email = "testdupe@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.delete(f"/activities/{activity}/unregister", params={"email": email})

# Arrange-Act-Assert: Test unregistering a participant
def test_unregister_success():
    # Arrange
    email = "testremove@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]

# Arrange-Act-Assert: Test error on unregistering non-existent participant
def test_unregister_not_found():
    # Arrange
    email = "idontexist@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

# Arrange-Act-Assert: Test error on non-existent activity
def test_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Activity"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
