import pytest

from users.models import User


@pytest.fixture
def data():
    data = {"email": "testuser@example.com", "password": "12345678"}
    return data


@pytest.fixture
def user(data):
    return User.objects.create_user(**data)


@pytest.mark.django_db
def test_user_has_been_created_with_email(user, data):
    assert user.email == data["email"]
