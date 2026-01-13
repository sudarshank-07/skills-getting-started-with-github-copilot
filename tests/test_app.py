import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure not already signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    print('Signup response:', response.status_code, response.text)
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Check participant is added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]
    # Unregister
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]
    # Check participant is removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]

def test_signup_duplicate():
    activity = "Programming Class"
    email = "emma@mergington.edu"  # already signed up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_unregister_not_found():
    activity = "Programming Class"
    email = "notfound@mergington.edu"
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
print(response.status_code, response.text)
