def test_root_redirects_to_static_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Mergington High School" in response.text


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert activities["Chess Club"]["max_participants"] == 12
    assert "participants" in activities["Chess Club"]
    assert isinstance(activities["Chess Club"]["participants"], list)


def test_signup_for_activity_success(client):
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Art Club/signup", params={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {email} for Art Club"

    activities = client.get("/activities").json()
    assert email in activities["Art Club"]["participants"]


def test_signup_for_activity_duplicate_returns_400(client):
    email = "michael@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_for_nonexistent_activity_returns_404(client):
    response = client.post("/activities/Nonexistent/signup", params={"email": "student@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_success(client):
    email = "michael@mergington.edu"
    response = client.delete("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_not_signed_up_returns_400(client):
    email = "notregistered@mergington.edu"
    response = client.delete("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_nonexistent_activity_returns_404(client):
    response = client.delete("/activities/Nonexistent/signup", params={"email": "student@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
