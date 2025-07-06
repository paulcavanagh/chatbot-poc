import unittest
from fastapi.testclient import TestClient
from app.main import app
import json

class TestUserRoute(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_user_found(self):
        # Mock Redis: Insert a user directly using the app's redis_client
        from app.redis_client import r
        user_id = 12345
        user_data = {"personName": "Test User", "nationality": "Irish"}
        key = f"user:{user_id}"
        r.set(key, json.dumps(user_data))

        response = self.client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["personName"] == "Test User"
        assert response.json()["nationality"] == "Irish"

    def test_get_user_not_found(self):
        response = self.client.get("/users/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

if __name__ == "__main__":
    unittest.main()
