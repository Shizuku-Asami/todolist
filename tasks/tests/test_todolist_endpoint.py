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
def test_create_todolist_with_minimal_data_returns_http_201_created(
    auth_client, data, user
):
    data["user"] = user.id
    response = auth_client.post("/todolists/", data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_todolist_with_at_least_one_todoitem_returns_http_201_created(
    auth_client, data_extra, user
):
    data_extra["user"] = user.id
    response = auth_client.post("/todolists/", data_extra)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_todolist_with_many_todoitems_returns_http_201_created(
    auth_client, data_extra1, user
):
    data_extra1["user"] = user.id
    response = auth_client.post("/todolists/", data_extra1)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_todolist_without_todoitems_returns_valid_response(
    auth_client, data, user
):
    data["user"] = user.id
    response = auth_client.post("/todolists/", data)
    LOGGER.info("Response data: %s", response.data)
    for key in data.keys():
        assert key in response.data.keys()
        assert data[key] == response.data[key]


@pytest.mark.django_db
def test_create_todolist_with_one_todoitem_returns_valid_response(
    auth_client, data_extra, user
):
    data_extra["user"] = user.id
    response = auth_client.post("/todolists/", data_extra)
    LOGGER.info("Response data: %s", response.data)
    for key in data_extra.keys():
        if key == "todoitem_todolist":
            for i in data_extra[key]:
                assert i in response.data[key].keys()
                assert data_extra[key][i] == response.data[key][i]
        else:
            assert key in response.data.keys()
            assert data_extra[key] == response.data[key]


@pytest.mark.django_db
def test_create_todolist_with_todoitems_returns_valid_response(
    auth_client, data_extra1, user
):
    data_extra1["user"] = user.id
    response = auth_client.post("/todolists/", data_extra1)
    LOGGER.info("Response data: %s", response.data)
    for key in data_extra1.keys():
        if key == "todoitem_todolist":
            for i in data_extra1[key]:
                assert i in response.data[key].keys()
                assert data_extra1[key][i] == response.data[key][i]
        else:
            assert key in response.data.keys()
            assert data_extra1[key] == response.data[key]


@pytest.mark.django_db
def test_get_todolist_returns_http_200_ok(auth_client, user):
    pass


@pytest.mark.django_db
def test_get_all_todolist_for_current_user(auth_client, user):
    response = auth_client.get("/todolists/")
    LOGGER.info("Response data: %s", response.data)


@pytest.mark.django_db
def test_update_todolist_name_returns_http_200_ok(auth_client, user):
    pass


@pytest.mark.django_db
def test_update_todolist_name_returns_updated_todolist(auth_client, user):
    pass


@pytest.mark.django_db
def test_update_todolist_description_returns_http_200_ok(auth_client, user):
    pass


@pytest.mark.django_db
def test_update_todolist_description_returns_updated_todolist(auth_client, user):
    pass


@pytest.mark.django_db
def test_update_todolist_todoitems_returns_http_200_ok(auth_client, user):
    pass


@pytest.mark.django_db
def test_update_todolist_todoitems_returns_updated_todolist(auth_client, user):
    pass


@pytest.mark.django_db
def test_update_todolist_multiple_fields_returns_http_200_ok(auth_client, user):
    pass


@pytest.mark.django_db
def test_update_todolist_multiple_fields_returns_updated_todolist(auth_client, user):
    pass


@pytest.mark.django_db
def test_delete_todolist_returns_http_200_ok(auth_client, user):
    pass


@pytest.mark.django_db
def test_delete_todolist_removes_todolist_data_from_database(auth_client, client):
    pass


@pytest.mark.django_db
def test_user_cannot_create_todolist_for_another_user(auth_client, user):
    pass


@pytest.mark.django_db
def test_user_cannot_get_todolist_of_another_user(auth_client, user):
    pass


@pytest.mark.django_db
def test_user_cannot_update_todolist_of_another_user(auth_client, user):
    pass


@pytest.mark.django_db
def test_user_cannot_delete_todolist_of_another_user(auth_client, user):
    pass
