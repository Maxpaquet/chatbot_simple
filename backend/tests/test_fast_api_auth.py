from fastapi.testclient import TestClient

from chatbot.api.main import app


def test_token_route():
    with TestClient(app) as client:
        # These credentials must match a user in fake_users_db
        data = {"username": "johndoe", "password": "secret"}
        response = client.post("/token", data=data)
        assert response.status_code == 200
        json_data = response.json()
        print(json_data)
        assert "access_token" in json_data
        assert json_data["token_type"] == "bearer"


def test_protected_route():
    with TestClient(app) as client:
        # Get token first
        data = {"username": "johndoe", "password": "secret"}
        token_response = client.post("/token", data=data)
        assert token_response.status_code == 200
        print(token_response.json())
        access_token = token_response.json()["access_token"]
        print(access_token)

        # Access protected route
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/protected", headers=headers)
        assert response.status_code == 200
        json_data = response.json()
        print(json_data)
        assert "message" in json_data
        assert "johndoe" in json_data["message"]


if __name__ == "__main__":
    # test_token_route()
    test_protected_route()
