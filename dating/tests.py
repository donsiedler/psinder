import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_create(user_create):
    assert User.objects.all().count() == 1
    assert User.objects.get(username="test_user") == user_create


def test_user_registration_form_view(client):
    response = client.get("/register/")
    assert response.status_code == 200


data = {
    "username": "test_user",
    "password1": "T3st_p@$$word",
    "password2": "T3st_p@$$word",
    "gender": 0,
    "dob": "1990-01-01",
}


@pytest.mark.django_db
def test_user_registration_form_creates_user(client):
    response = client.post("/register/", data)
    assert response.status_code == 302
    assert User.objects.all().count() == 1
    assert User.objects.filter(username="test_user").exists()


@pytest.mark.django_db
def test_user_can_login(client, user_create):
    response = client.post("/login/", {"username": "test_user", "password": "T3st_p@$$word"})
    assert response.status_code == 302
    assert client.login(username="test_user", password="T3st_p@$$word")


@pytest.mark.django_db
def test_user_can_logout(client):
    response = client.get("/logout/")
    assert response.status_code == 302
    assert response.url == "/"
