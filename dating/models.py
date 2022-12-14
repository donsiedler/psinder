from django.contrib.auth.models import AbstractUser
from django.db import models
from dogs.models import Dog


class Address(models.Model):
    city = models.CharField(max_length=30)
    post_code = models.CharField(max_length=6)
    street = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.street} {self.post_code} {self.city}"


GENDERS = (
    (0, "kobieta"),
    (1, "mężczyzna")
)


class User(AbstractUser):
    gender = models.PositiveSmallIntegerField(choices=GENDERS, verbose_name="Płeć")
    dob = models.DateField(verbose_name="Data urodzenia")
    bio = models.TextField(null=True, blank=True, verbose_name="Twój opis")
    photo = models.ImageField(upload_to="user_image",
                              default="default_avatar.png",
                              verbose_name="Zdjęcie profilowe")
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name="Numer telefonu")
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True, verbose_name="Adres")
    slug = models.SlugField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = self.username

    def __str__(self):
        return self.username

    def get_user_dogs(self):
        return Dog.objects.filter(owner=self)

    def get_user_meetings(self):
        return Meeting.objects.filter(participating_users=self)


class Meeting(models.Model):
    date = models.DateField()
    time = models.TimeField()
    max_users = models.PositiveSmallIntegerField()
    max_dogs = models.PositiveSmallIntegerField()
    target_user_gender = models.PositiveSmallIntegerField(choices=GENDERS, null=True, blank=True)
    target_user_age = models.PositiveSmallIntegerField(null=True, blank=True)
    target_dog_sex = models.PositiveSmallIntegerField(choices=GENDERS, null=True, blank=True)
    target_dog_age = models.PositiveSmallIntegerField(null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    notes = models.TextField(null=True, blank=True)
    date_time_created = models.DateTimeField(auto_now_add=True)
    participating_dogs = models.ManyToManyField(Dog, related_name="dogs")
    participating_users = models.ManyToManyField(User, related_name="users")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_meeting_users_count(self):
        return self.participating_users.count()

    def get_meeting_dogs_count(self):
        return self.participating_dogs.count()
