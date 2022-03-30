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


@pytest.mark.django_db
def test_user_email_field_label(user):
    assert user._meta.get_field("email").verbose_name == "email address"


@pytest.mark.django_db
def test_user_password_field_label(user):
    assert user._meta.get_field("password").verbose_name == "password"


@pytest.mark.django_db
def test_user_email_field_max_length(user):
    assert user._meta.get_field("email").max_length == 254


@pytest.mark.django_db
def test_user_created_is_active_returns_true(user):
    assert user.is_active == True


@pytest.mark.django_db
def test_user_created_is_staff_returns_false(user):
    assert user.is_staff == False


@pytest.mark.django_db
def test_user_created_is_admin_returns_false(user):
    assert user.is_admin == False


@pytest.mark.django_db
def test_user_model_manager_name(user):
    assert (
        user.__class__.__dict__["objects"].__dict__["manager"].__class__.__name__
        == "UserManager"
    )


@pytest.mark.django_db
def test_user_model_number_of_fields(user):
    assert len(user._meta.fields) == 8


@pytest.mark.django_db
def test_user_model_field_names(user):
    user_fields = [field.name for field in User._meta.fields]
    assert set(user_fields) == set([
        "id",
        "password",
        "last_login",
        "is_superuser",
        "email",
        "is_active",
        "is_admin",
        "is_staff",
    ])
