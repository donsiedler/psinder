import pytest
from dating.conftest import new_user1, new_user_factory
from .models import Dog


def test_user_can_add_dog(new_user1, client):
    user = new_user1
    data = {
        "name": "test_dog",
        "age": 3,
        "sex": 0,
        "breed": "test",
        "size": 2,
        "bio": "test",
        "owner": user.pk,
    }
    client.login(username="test_user", password="T3st_p@$$word")
    response = client.get("/add_dog/")
    assert response.status_code == 200
    response = client.post("/add_dog/", data=data)
    assert response.status_code == 302
    assert Dog.objects.all().count() == 1
    assert Dog.objects.all().first().owner == user


def test_user_can_edit_dog(new_dog, client):
    data = {
        "name": "my_test_dog",
        "age": 2,
        "sex": 1,
        "breed": "mixed",
        "size": 3,
        "bio": "Short story",
    }
    client.login(username="test_user", password="T3st_p@$$word")
    response = client.get(f"/dog_profile/{new_dog.pk}/edit/")
    assert response.status_code == 200
    response = client.post(f"/dog_profile/{new_dog.pk}/edit/", data=data)
    assert response.status_code == 302
    assert response.url == "/dogs/"
    dog = Dog.objects.first()
    assert dog.name == "my_test_dog"
    assert dog.breed == "mixed"
    assert dog.size == 3


def test_user_can_view_dog_profile(new_dog, client):
    client.login(username="test_user", password="T3st_p@$$word")
    response = client.get(f"/dog_profile/{new_dog.pk}/")
    assert response.status_code == 200
    assert response.context["object"] == new_dog
    assert response.context["object"].bio == "test"


def test_user_can_search_dogs_profiles(new_dog, client):
    client.login(username="test_user", password="T3st_p@$$word")
    response = client.get("/profiles_search/")
    assert response.status_code == 200
    response = client.post("/profiles_search/", data={"query": "test"})
    assert response.context["dog_profiles"].count() == 1
