from faker import Faker


def create_profile():
    """
    Generates a fake profile data to create fake users in the app
    :return:
    """
    fake = Faker("pl-PL")
    profile = fake.profile()
    username = profile.get("username")
    email = profile.get("mail")
    password = fake.password()
    name = profile.get("name")
    first_name = name.split(" ")[0]
    last_name = name.split(" ")[1]
    gender = 0 if first_name[-1] == "a" else 1  # If name ends with "a" assume it's 0 for female
    dob = profile.get("birthdate")
    return username, email, password, first_name, last_name, gender, dob


print(create_profile())
