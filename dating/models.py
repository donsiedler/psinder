from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDERS = (
        (0, "female"),
        (1, "male")
    )

    gender = models.PositiveSmallIntegerField(choices=GENDERS)
    dob = models.DateField()
    bio = models.TextField(null=True)
    photo = models.ImageField(upload_to="dating/static_files/uploads/",
                              default="dating/static_files/default_avatar.png")
    phone = models.CharField(max_length=12, null=True)

    def __str__(self):
        return self.username
