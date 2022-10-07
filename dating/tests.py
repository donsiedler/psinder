import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

User = get_user_model()


class Forbidden(Exception):
    pass


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
def test_user_registration_form_creates_user_and_redirects_to_dashboard(client):
    response = client.post("/register/", data)
    assert response.status_code == 302
    assert User.objects.all().count() == 1
    assert User.objects.filter(username="test_user").exists()
    assert response.url == "/dashboard/"


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


def test_view_user_profile(user_create, client):
    client.login(username="test_user", password="T3st_p@$$word")
    response = client.get("/dashboard/")
    assert response.status_code == 200


def test_view_user_settings_profile(user_create, client):
    user = user_create
    client.login(username="test_user", password="T3st_p@$$word")
    response = client.get(f"/settings/{user.pk}/")
    assert response.status_code == 200
    assert user == response.context_data["object"]


@pytest.mark.django_db
def test_user_can_change_settings(user_create, client):
    user = user_create
    client.login(username="test_user", password="T3st_p@$$word")
    data = {
        "first_name": "test_name",
        "bio": "Lorem ipsum",
        "gender": 1,
        "dob": "1991-07-01"
    }
    response = client.post(f"/settings/{user.pk}/", data)
    assert response.status_code == 302
    user = User.objects.all().first()
    assert user.first_name == "test_name"
    assert user.bio == "Lorem ipsum"
    assert user.gender == 1
    assert str(user.dob) == "1991-07-01"


@pytest.mark.django_db
def test_user_can_change_address(user_create, client):
    user = user_create
    client.login(username="test_user", password="T3st_p@$$word")
    data = {
        "street": "Sezamkowa",
        "city": "New York",
        "post_code": "00-000",
    }
    response = client.post(f"/settings/{user.pk}/change_address/", data)
    assert response.status_code == 302
    user = User.objects.all().first()
    assert user.address
    assert user.address.street == "Sezamkowa"
    assert user.address.city == "New York"
    assert user.address.post_code == "00-000"


def test_user_can_change_password(user_create, client):
    user = user_create
    client.login(username="test_user", password="T3st_p@$$word")
    data = {
        "new_password": "new_T3st_p@$$word",
        "new_password2": "new_T3st_p@$$word",
    }
    response = client.post(f"/settings/{user.pk}/change_password/", data)
    assert response.status_code == 302
    client.get("/logout/")
    client.login(username="test_user", password="new_T3st_p@$$word")
    assert user.is_authenticated


@pytest.mark.parametrize("url, status_code, redirect_url", (
        ("/dashboard/", 302, "/login/?next=/dashboard/"),
        ("/profiles_search/", 302, "/login/?next=/profiles_search/"),
        ("/meetings/", 302, "/login/?next=/meetings/"),
        ("/add_meeting/", 302, "/login/?next=/add_meeting/"),
        ("/meetings/search/", 302, "/login/?next=/meetings/search/"),
        ("/add_dog/", 302, "/login/?next=/add_dog/"),
        ("/dogs/", 302, "/login/?next=/dogs/"),
        ("/inbox/", 302, "/login/?next=/inbox/"),
        ("/inbox/create_thread/", 302, "/login/?next=/inbox/create_thread/"),
))
def test_user_cannot_access_restricted_views_without_login(client, url, status_code, redirect_url):
    response = client.get(url)
    assert response.status_code == status_code
    assert response.url == redirect_url


@pytest.mark.django_db
def test_user_cannot_edit_other_users_settings(new_user1, new_user2, client):
    user2 = new_user2
    client.login(username="test_user", password="T3st_p@$$word")
    assert client.get(f"/settings/{user2.pk}/").status_code == 403
    assert client.get(f"/settings/{user2.pk}/change_address/").status_code == 403
    assert client.get(f"/settings/{user2.pk}/change_password/").status_code == 403


@pytest.mark.django_db
def test_user_can_view_other_users_profiles(new_user1, new_user2, client):
    user2 = new_user2
    client.login(username="test_user", password="T3st_p@$$word")
    response = client.get(f"/profile/{user2.slug}/")
    assert response.status_code == 200
    assert response.context["user_profile"] == user2


@pytest.mark.django_db
def test_user_can_search_users_profiles(new_user1, new_user2, client):
    client.login(username="test_user", password="T3st_p@$$word")
    response = client.get("/profiles_search/")
    assert response.status_code == 200
    response = client.post("/profiles_search/", data={"query": "test"})
    assert response.context["user_profiles"].count() == 2
