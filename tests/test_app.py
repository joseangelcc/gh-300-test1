from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_rejects_duplicate_email():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    first_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert first_response.status_code == 200

    duplicate_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student already signed up for this activity"


def test_delete_participant_removes_email():
    activity_name = "Chess Club"
    email = "remove.me@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    assert delete_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]
