import pytest
from django.test import Client
from rest_framework import status

from ..models import User


@pytest.fixture
def data():
    data = {"email": "testuser@example.com", "password": "12345678"}
    return data


@pytest.fixture
def user(data):
    user = User.objects.create_user(**data)
    return user

@pytest.fixture
def client():
    client = Client(
        enforce_csrf_checks=True,
        HTTP_USER_AGENT="Mozilla/5.0",
    )
    return client


@pytest.mark.django_db
def test_valid_user_credentials_returns_http_200_ok(client, data, user):
    response = client.post("/users/login", data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_non_valid_user_credentials_returns_http_401_unauthorized(client, data, user):
    data["password"] = "wrongpassword"
    response = client.post("/users/login", data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_empty_password_field_returns_http_400_bad_request(client, data, user):
    data["password"] = ""
    response = client.post("/users/login", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_empty_email_field_returns_http_400_bad_request(client, data, user):
    data["email"] = ""
    response = client.post("/users/login", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_non_valid_email_field_returns_http_400_bad_request(client, data, user):
    data["email"] = "nonvalid"
    response = client.post("/users/login", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_wrong_email_field_returns_http_401_unauthorized(client, data, user):
    data["email"] = "user@example.com"
    response = client.post("/users/login", data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_shorter_than_min_length_password_returns_http_400_bad_request(client, data, user):
    data["password"] = "short"
    response = client.post("/users/login", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST