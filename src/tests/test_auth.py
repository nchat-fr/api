from fastapi.testclient import TestClient
from src.tests import app
from src.tests.datasets import dataset

from sqlalchemy import select
from src.models import Users
from src.utils.webtokens import logged_as

client = TestClient(app)


def test_logged_as(dataset):
    url = f"/auth/"

    response = client.get(url)
    assert response.status_code == 403

    with logged_as(client, dataset.user_1):
        response = client.get(url)
        assert response.status_code == 200
        assert response.json()["id"] == dataset.user_1.id


def test_register(dataset):
    url = f"/auth/register"

    response = client.post(url)
    assert response.status_code == 422

    data = {"password": "0000"}
    response = client.post(url, json=data)
    assert response.status_code == 422

    data = {"mail": "", "username": "", "password": "0000"}
    response = client.post(url, json=data)
    assert response.status_code == 422

    data = {"mail": "test@pytest.io", "username": "cool_tester", "password": "0000"}
    response = client.post(url, json=data)
    result = dataset.session.scalars(
        select(Users).where(Users.mail == data["mail"])
    ).first()
    assert response.status_code == 201
    assert result is not None


def test_login(dataset):
    url = f"/auth/login"

    response = client.post(url)
    assert response.status_code == 422

    data = {"password": "0000"}
    response = client.post(url, json=data)
    assert response.status_code == 422

    data = {"mail": dataset.user_1.mail, "password": dataset.user_1.password_nonhashed}
    response = client.post(url, json=data)
    assert response.status_code == 200
    assert client.cookies.get("authenticator") is not None


def test_logout(dataset):
    url = "/auth/"

    # be sure to not be logged
    client.cookies = None
    response = client.delete(url)
    assert response.status_code == 403

    with logged_as(client, dataset.user_1):
        response = client.delete(url)
        assert response.status_code == 204
