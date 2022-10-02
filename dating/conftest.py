import pytest
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user_create():
    user = User.objects.create_user(
        username="test_user",
        email="test@test.com",
        password="T3st_p@$$word",
        first_name="test",
        gender=0,
        dob="1990-01-01",
    )
    return user
