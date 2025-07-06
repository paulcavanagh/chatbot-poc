import unittest
from fastapi.testclient import TestClient
from app.main import app
import json

class TestUserLicenceTypeRoute(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        from app.redis_client import r
        self.r = r

    def test_get_users_by_licence_type(self):
        # Clear all users first
        for key in self.r.keys("user:*"):
            self.r.delete(key)
        # Add users with different licence types
        user1 = {"personName": "Alice", "licenceType": "A"}
        user2 = {"personName": "Bob", "licenceType": "B"}
        user3 = {"personName": "Charlie", "licenceType": "A"}
        self.r.set("user:1", json.dumps(user1))
        self.r.set("user:2", json.dumps(user2))
        self.r.set("user:3", json.dumps(user3))
        # Query for licenceType A
        response = self.client.get("/users/by-licence-type/?licence_type=A")
        assert response.status_code == 200
        users = response.json()
        assert any(u["personName"] == "Alice" for u in users)
        assert any(u["personName"] == "Charlie" for u in users)
        assert all(u["licenceType"] == "A" for u in users)
        # Query for licenceType B
        response = self.client.get("/users/by-licence-type/?licence_type=B")
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 1
        assert users[0]["personName"] == "Bob"
        assert users[0]["licenceType"] == "B"

if __name__ == "__main__":
    unittest.main()
