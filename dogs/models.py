from django.db import models


class Dog(models.Model):
    SIZES = (
        (0, "small"),  # <5 kg
        (1, "medium"),  # <20 kg
        (2, "large"),  # <40 kg
        (3, "giant"),  # >40 kg
    )

    GENDERS = (
        (0, "female"),
        (1, "male")
    )

    name = models.CharField(max_length=32, verbose_name="Imię")
    age = models.PositiveSmallIntegerField(verbose_name="Wiek")
    sex = models.PositiveSmallIntegerField(choices=GENDERS, verbose_name="Płeć")
    breed = models.CharField(max_length=64, verbose_name="Rasa")
    size = models.PositiveSmallIntegerField(choices=SIZES, verbose_name="Wielkość psa")
    bio = models.TextField(null=True, verbose_name="Opis")
    photo = models.ImageField(upload_to="dog_image",
                              default="default_avatar.png",
                              verbose_name="Zdjęcie psa")
    owner = models.ForeignKey("dating.User", on_delete=models.CASCADE)
