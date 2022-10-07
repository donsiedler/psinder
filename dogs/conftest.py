import pytest
from dating.conftest import new_user1
from .models import Dog


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
