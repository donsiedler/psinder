import random

import pytest
from faker import Faker
from pytest_factoryboy import register
from django.contrib.auth import get_user_model
from django.test import Client

from dogs.models import Dog
from .factories import UserFactory
from .models import Meeting, Address

register(UserFactory)

User = get_user_model()
fake = Faker()


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


@pytest.fixture
def new_address(db):
    return Address.objects.create(city=fake.city())


@pytest.fixture
def new_dog(db, new_user1):
    dog = Dog.objects.create(
        name="test_dog",
        age=3,
        sex=0,
        breed="test",
        size=2,
        bio="test",
        owner=new_user1
    )
    return dog


@pytest.fixture
def new_meeting(db, new_dog, new_address, client):
    client.login(username="test_user", password="T3st_p@$$word")
    meeting = Meeting.objects.create(
        date=fake.date(),
        time=fake.time(),
        max_users=random.randint(2, 10),
        max_dogs=random.randint(0, 10),
        address=new_address,
        created_by=new_dog.owner,
    )
    meeting.participating_dogs.add(new_dog)
    return meeting
