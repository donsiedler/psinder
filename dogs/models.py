from django.db import models

from dating.models import User


class Dog(models.Model):
    SIZES = (
        (0, "small"),  # <5 kg
        (1, "medium"),  # <20 kg
        (2, "large"),  # <40 kg
        (3, "giant"),  # >40 kg
    )

    name = models.CharField(max_length=32)
    age = models.PositiveSmallIntegerField()
    sex = models.PositiveSmallIntegerField(choices=User.GENDERS)
    breed = models.CharField(max_length=64)
    size = models.PositiveSmallIntegerField(choices=SIZES)
    bio = models.TextField(null=True)
    photo = models.ImageField(upload_to="dogs/static_files/uploads/",
                              default="dogs/static_files/default_avatar.png")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
