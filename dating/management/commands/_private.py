from faker import Faker
from django.contrib.auth import get_user_model

User = get_user_model()


def create_fake_user():
    """
    Generates a fake user with Polish locale and saves it to dating_user table
    :return: None
    """
    fake = Faker("pl-PL")
    profile = fake.profile()

    username = profile.get("username")
    email = profile.get("mail")
    password = fake.password()
    name = profile.get("name").split(" ")
    if name[0] == "pani" or name[0] == "pan":  # Remove the titles
        del name[0]
    first_name = name[0]
    last_name = name[1]
    gender = 0 if first_name[-1] == "a" else 1  # If name ends with "a" assume it's 0 for female
    dob = profile.get("birthdate")

    User.objects.create_user(username=username,
                             email=email,
                             password=password,
                             first_name=first_name,
                             last_name=last_name,
                             gender=gender,
                             dob=dob)
