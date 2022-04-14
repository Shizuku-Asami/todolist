import pytest
from django.test import Client
from rest_framework import status
import logging

from users.models import User
from tasks.models import TodoList, TodoItem


LOGGER = logging.getLogger(__name__)


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
        "todoitem_todolist": [],
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
        "todoitem_todolist": [
            {
                "name": "item 1",
                "description": "easy",
                "is_done": False,
            },
        ],
    }
    return data


@pytest.fixture
def data_extra1():
    """
    Todolist data with todoitems.
    """
    data = {
        "name": "test todolist",
        "description": "A description for the new todolist",
        "todoitem_todolist": [
            {
                "name": "item 1",
                "description": "easy",
                "is_done": False,
            },
            {
                "name": "item 2",
                "description": "medium",
                "is_done": False,
            },
        ],
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
@pytest.mark.django_db
def auth_client(client, login_data, user):
    response = client.post("/users/login", login_data)
    access_token = response.data["tokens"]["access"]
    headers = {"HTTP_AUTHORIZATION": "Bearer " + access_token}
    client.defaults = headers
    return client


@pytest.mark.django_db
def test_create_todolist_with_minimal_data(auth_client, data, user):
    data["user"] = user.id
    response = auth_client.post("/todolists/", data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_todolist_with_at_least_one_todoitem(auth_client, data_extra, user):
    data_extra["user"] = user.id
    response = auth_client.post("/todolists/", data_extra)
    assert response.status_code == status.HTTP_201_CREATED