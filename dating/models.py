from django.contrib.auth.models import AbstractUser
from django.db import models


class Address(models.Model):
    city = models.CharField(max_length=30)
    post_code = models.CharField(max_length=6)
    street = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.post_code}, {self.city}, {self.street}"


class User(AbstractUser):
    GENDERS = (
        (0, "female"),
        (1, "male")
    )

    gender = models.PositiveSmallIntegerField(choices=GENDERS, verbose_name="Płeć")
    dob = models.DateField(verbose_name="Data urodzenia")
    bio = models.TextField(null=True, blank=True, verbose_name="Twój opis")
    photo = models.ImageField(upload_to="user_image",
                              default="default_avatar.png",
                              verbose_name="Zdjęcie profilowe")
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name="Numer telefonu")
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True, verbose_name="Adres")

    def __str__(self):
        return self.username
