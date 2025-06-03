import sys, os; sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_index_page():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]

def test_create_user():
    resp = client.post("/users", json={"username": "alice"})
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data
    assert data["username"] == "alice"

def test_upload_video_and_feed(tmp_path):
    # create user
    user_resp = client.post("/users", json={"username": "bob"})
    user_id = user_resp.json()["id"]

    # create a dummy video file
    video_file = tmp_path / "video.mp4"
    video_file.write_bytes(b"0" * 10)

    with video_file.open("rb") as f:
        resp = client.post(
            "/videos",
            data={"user_id": user_id, "description": "test"},
            files={"file": ("video.mp4", f, "video/mp4")},
        )
    assert resp.status_code == 200
    video_id = resp.json()["id"]

    feed_resp = client.get("/feed")
    assert feed_resp.status_code == 200
    assert any(v["id"] == video_id for v in feed_resp.json())
