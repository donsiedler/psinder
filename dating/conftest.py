import pytest
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user_create(db):
    user = User.objects.create_user(
        username="test_user",
        email="test@test.com",
        password="T3st_p@$$word",
        first_name="test",
        gender=0,
        dob="1990-01-01",
    )
    return user


@pytest.fixture
def new_user_factory(db):
    def create_app_user(
            username,
            password="T3st_p@$$word",
            first_name="test",
            gender=0,
            email="test@test.com",
            dob="1990-01-01",
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            gender=gender,
            email=email,
            dob=dob,
        )
        return user

    return create_app_user


@pytest.fixture
def new_user1(db, new_user_factory):
    return new_user_factory("test_user")


@pytest.fixture
def new_user2(db, new_user_factory):
    return new_user_factory("test_user2")
