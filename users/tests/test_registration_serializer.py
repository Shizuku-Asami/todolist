import pytest

from users.serializers import RegistrationSerializer
from users.models import User


@pytest.fixture
def data():
    data = {"email": "testuser@example.com", "password": "12345678"}
    return data


@pytest.fixture
def serializer(data):
    serializer = RegistrationSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer


def test_has_expected_fields(data, serializer):
    assert set(serializer.data.keys()) == set(["email"])


def test_email_field_has_expected_value(data, serializer):
    assert serializer.data.get("email") == data["email"]


def test_data_has_invalid_email(data):
    data["email"] = "invalid"
    serializer = RegistrationSerializer(data=data)
    assert serializer.is_valid() == False


def test_data_has_invalid_password(data):
    data["password"] = ""
    serializer = RegistrationSerializer(data=data)
    assert serializer.is_valid() == False


def test_data_has_invalid_password_less_than_min_len(data):
    data["password"] = "123"
    serializer = RegistrationSerializer(data=data)
    assert serializer.is_valid() == False


def test_data_has_invalid_password_greater_than_max_len(data):
    data["password"] = "long" * 10
    serializer = RegistrationSerializer(data=data)
    assert serializer.is_valid() == False
