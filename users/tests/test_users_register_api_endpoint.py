import pytest
from django.test import Client
from rest_framework import status


@pytest.fixture
def data():
    data = {"email": "testuser@example.com", "password": "12345678"}
    return data


@pytest.fixture
def client():
    client = Client(
        enforce_csrf_checks=True,
        HTTP_USER_AGENT="Mozilla/5.0",
    )
    return client


@pytest.mark.django_db
def test_valid_payload_returns_http_201_created(client, data):
    response = client.post("/users/register", data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_invalid_email_returns_http_400_bad_request_with_code_invalid(client, data):
    data["email"] = "invalid"
    response = client.post("/users/register", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert set(response.data.keys()) == set(["email"])
    assert response.data["email"][0].code == "invalid"
    assert response.data["email"][0][:] == "Enter a valid email address."


@pytest.mark.django_db
def test_empty_email_returns_http_400_bad_request_with_code_blank(client, data):
    data["email"] = ""
    response = client.post("/users/register", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert set(response.data.keys()) == set(["email"])
    assert response.data["email"][0].code == "blank"
    assert response.data["email"][0][:] == "This field may not be blank."


@pytest.mark.django_db
def test_short_password_returns_http_400_bad_request_with_code_min_length(client, data):
    data["password"] = "123"
    response = client.post("/users/register", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert set(response.data.keys()) == set(["password"])
    assert response.data["password"][0].code == "min_length"
    assert (
        response.data["password"][0][:]
        == "Ensure this field has at least 8 characters."
    )


@pytest.mark.django_db
def test_long_password_returns_http_400_bad_request_with_code_max_length(client, data):
    data["password"] = "long" * 10
    response = client.post("/users/register", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert set(response.data.keys()) == set(["password"])
    assert response.data["password"][0].code == "max_length"
    assert (
        response.data["password"][0][:]
        == "Ensure this field has no more than 32 characters."
    )


@pytest.mark.django_db
def test_empty_email_returns_http_400_bad_request_with_code_blank(client, data):
    data["password"] = ""
    response = client.post("/users/register", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert set(response.data.keys()) == set(["password"])
    assert response.data["password"][0].code == "blank"
    assert response.data["password"][0][:] == "This field may not be blank."
