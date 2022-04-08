import pytest
from django.test import Client
from rest_framework import status

from users.models import User
from tasks.models import TodoList


@pytest.fixture
def login_data():
    data = {
        "email": "testuser@example.com",
        "password": "12345678",
    }
    return data


@pytest.fixture
def data():
    """
    Minimal data to create a todolist object in the database.
    """
    data = {
        "name": "test todolist",
        "description": "A description for the new todolist",
    }
    return data


@pytest.fixture
def data_extra():
    """
    Todolist data with todoitems.
    """
    data = {
        "name": "test todolist",
        "description": "A description for the new todolist",
        "todoitem_todolist": {
            "name": "item 1",
            "description": "easy",
            "is_done": False,
        },
    }
    return data


@pytest.fixture
def user():
    return User.objects.create_user(email="testuser@example.com", password="12345678")


@pytest.fixture
def client():
    client = Client(
        enforce_csrf_checks=True,
        HTTP_USER_AGENT="Mozilla/5.0",
    )
    return client


@pytest.fixture
def auth_client(client, login_data):
    response = client.get("/users/login", **login_data)
    access_token = response.data["tokens"]["access"]
    headers = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
    client.defaults = headers
    return client


@pytest.mark.django_db
def test_create_todolist_with_minimal_data(auth_client, data):
    response = auth_client.post("/todolists/", data)
    assert response.status_code == status.HTTP_201_CREATED
