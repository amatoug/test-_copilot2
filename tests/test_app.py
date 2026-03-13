import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# AAA: Arrange-Act-Assert

def test_get_activities():
    # Arrange
    # (client is ready)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_and_remove_participant():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    signup_resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert signup_resp.status_code == 200
    assert email in signup_resp.json()["message"]

    # Act (remove)
    remove_resp = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert remove_resp.status_code == 200
    assert email in remove_resp.json()["message"]


def test_signup_twice_should_fail():
    # Arrange
    activity = "Programming Class"
    email = "double@mergington.edu"
    # Act
    client.post(f"/activities/{activity}/signup", params={"email": email})
    second_resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert second_resp.status_code == 400
    assert "already signed up" in second_resp.json()["detail"]


def test_remove_nonexistent_participant():
    # Arrange
    activity = "Gym Class"
    email = "notfound@mergington.edu"
    # Act
    resp = client.delete(f"/activities/{activity}/participants/{email}")
    # Assert
    assert resp.status_code == 404
    assert "Participant not found" in resp.json()["detail"]


def test_signup_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Activity"
    email = "ghost@mergington.edu"
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 404
    assert "Activity not found" in resp.json()["detail"]
