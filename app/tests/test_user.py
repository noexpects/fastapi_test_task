from fastapi.testclient import TestClient
from ..main import app

test_user = {
    "id": 1,
    "email": "example@mail.com",
    "password": "123",
    "username": "First",
    "PUT_email": "updated@mail.com",
    "PUT_password": "12345",
    "PUT_username": "UpdatedPUTFirst",
    "PATCH_username": "UpdatedPATCHFirst"
}

user_not_found_body = {
    "detail": "User not found"
}

user_already_exists_body = {
    "detail": "Email already registered"
}

bad_request_status_code = 404


def test_create_user(test_db):
    client = TestClient(app)
    response = client.post("/user/",
                           json={
                               "email": test_user["email"],
                               "password": test_user["password"],
                               "username": test_user["username"]
                           })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["username"] == test_user["username"]


def test_create_existing_user(test_db):
    client = TestClient(app)
    response = client.post("/user/",
                           json={
                               "email": test_user["email"],
                               "password": test_user["password"],
                               "username": test_user["username"]
                           })
    assert response.status_code == 400
    assert response.json() == user_already_exists_body


def test_get_user_by_id(test_db):
    client = TestClient(app)
    response = client.get(f"/user/{test_user['id']}")
    data = response.json()
    assert response.status_code == 200
    assert data["username"] == test_user["username"]
    assert data["id"] == test_user['id']


def test_update_user_data(test_db):
    client = TestClient(app)
    response = client.put(f"/user/{test_user['id']}",
                          json={
                              "email": test_user["PUT_email"],
                              "password": test_user["PUT_password"],
                              "username": test_user["PUT_username"]
                          })
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == test_user["id"]
    assert data["email"] == test_user["PUT_email"]


def test_partly_update_user_data(test_db):
    client = TestClient(app)
    response = client.patch(f"/user/{test_user['id']}",
                            json={
                                "username": test_user["PATCH_username"]
                            })
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == test_user["id"]
    assert data["username"] == test_user["PATCH_username"]


def test_user_delete(test_db):
    client = TestClient(app)
    response = client.delete(f"/user/{test_user['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == test_user["id"]


def test_get_user_that_does_not_exist(test_db):
    client = TestClient(app)
    response = client.get(f"/user/{test_user['id']}")
    assert response.status_code == bad_request_status_code
    assert response.json() == user_not_found_body


def test_update_user_that_does_not_exist(test_db):
    client = TestClient(app)
    response = client.put(f"/user/{test_user['id']}",
                          json={
                              "email": test_user["PUT_email"],
                              "password": test_user["PUT_password"],
                              "username": test_user["PUT_username"]
                          })
    assert response.status_code == bad_request_status_code
    assert response.json() == user_not_found_body


def test_partly_update_user_that_does_not_exist(test_db):
    client = TestClient(app)
    response = client.patch(f"/user/{test_user['id']}",
                            json={
                                "username": test_user["PATCH_username"]
                            })
    assert response.status_code == bad_request_status_code
    assert response.json() == user_not_found_body


def test_delete_user_that_does_not_exist(test_db):
    client = TestClient(app)
    response = client.delete(f"/user/{test_user['id']}")
    assert response.status_code == bad_request_status_code
    assert response.json() == user_not_found_body
