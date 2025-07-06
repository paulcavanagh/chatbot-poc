import unittest
from fastapi.testclient import TestClient
from app.main import app
import json

class TestUserRoute(unittest.TestCase):
  
    def setUp(self):
        self.client = TestClient(app)
        from app.redis_client import r
        self.r = r

    def test_get_all_user(self):
        # Clear all users first (for test isolation)
        for key in self.r.keys("user:*"):
            self.r.delete(key)
        # Add two users
        user1 = {"personName": "Alice", "nationality": "Irish"}
        user2 = {"personName": "Bob", "nationality": "French"}
        self.r.set("user:1", json.dumps(user1))
        self.r.set("user:2", json.dumps(user2))
        response = self.client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert any(u["personName"] == "Alice" for u in users)
        assert any(u["personName"] == "Bob" for u in users)
  
  
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
