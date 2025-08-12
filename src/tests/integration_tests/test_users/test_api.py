import pytest
from fastapi.testclient import TestClient

from src.auth.dao import UsersDAO


@pytest.mark.parametrize("first_name, last_name, email, password, password_repeat, status_code", [
    ("Иван", "Иванов", "user@user.com", "123", "123", 200),
    ("Иван", "Иванов", "user@user.com", "123", "123", 409),
    ("Магомед", "Магомедов", "user3@user3.com", "123", "123", 200),
    ("Иван", "Иванов", "sjdflsdjf", "123", "123", 422),
])
def test_register_user(first_name, last_name, email, password, status_code, password_repeat, client):
    response = client.post("/auth/register", json={
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "password_repeat": password_repeat,
    })

    assert response.status_code == status_code


def test_unauthorized_client(client: TestClient):
    current_client = client.get(
        "/auth/me",
    )
    assert current_client.status_code == 401


def test_client_and_admin_permissions(authenticated_client: TestClient, authenticated_admin: TestClient):
    current_client = authenticated_client.get(
        "/auth/me",
    )
    client_id = current_client.json()["id"]
    response = authenticated_client.patch(
        f"/auth/update/{client_id}",
        json={
            "middle_name": "Иванович"
        }
    )

    assert response.status_code == 200

    current_admin = authenticated_admin.get(
        "/auth/me",
    )
    admin_id = current_admin.json()["id"]
    response = authenticated_client.patch(
        f"/auth/update/{admin_id}",
        json={
            "middle_name": "Иванович"
        }
    )
    assert response.status_code == 403

    response = authenticated_admin.patch(
        f"/auth/update/{client_id}",
        json={
            "middle_name": "Иванович"
        }
    )
    assert response.status_code == 200


async def test_logout_client(client):
    client.post("/auth/register", json={
        "first_name": "Test",
        "last_name": "Test",
        "email": "test@mail.ru",
        "password": "test123",
        "password_repeat": "test123",
    })

    client.post("/auth/login", json={
        "email": "test@mail.ru",
        "password": "test123"
    })

    current_client = client.get(
        "/auth/me",
    )

    client_id = current_client.json()["id"]

    assert current_client.json()["is_active"] == True

    response = client.delete(
        f"/auth/delete/{client_id}"
    )

    assert response.status_code == 200

    current_client = client.get(
        "/auth/me",
    )
    assert current_client.status_code == 401

    user = await UsersDAO.find_by_id(client_id)

    assert user.is_active == False


def test_get_post(authenticated_client: TestClient, client: TestClient):
    response = client.get(
        "/posts"
    )
    assert response.status_code == 401

    response = authenticated_client.get(
        "/posts"
    )
    assert response.status_code == 200


def test_add_and_delete_post(authenticated_client: TestClient, authenticated_admin: TestClient):
    response = authenticated_admin.post(
        "/posts/add",
        json={"title": "Title"}
    )
    post_id = response.json()["id"]
    assert response.status_code == 201

    response = authenticated_client.delete(
        f"/posts/delete/{post_id}"
    )
    assert response.status_code == 403














