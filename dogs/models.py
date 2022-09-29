from django.db import models


class Dog(models.Model):
    SIZES = (
        (0, "mały"),  # <5 kg
        (1, "średni"),  # <20 kg
        (2, "duży"),  # <40 kg
        (3, "wielki"),  # >40 kg
    )

    GENDERS = (
        (0, "suczka"),
        (1, "pies")
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

    def __str__(self):
        return f"{self.name} ({self.breed})"
