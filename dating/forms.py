from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from dogs.models import Dog
from .models import Address, Meeting

User = get_user_model()

FORM_LABELS_PL = {
    "username": "Nazwa użytkownika",
    "email": "Adres email",
    "first_name": "Imię",
    "last_name": "Nazwisko",
    "gender": "Płeć",
    "dob": "Data urodzenia",
    "bio": "Opis profilu",
    "photo": "Zdjęcie profilowe",
    "phone": "Numer telefonu",
    "street": "Ulica",
    "city": "Miasto",
    "post_code": "Kod pocztowy",
}

POST_CODE_VALIDATOR_PL = RegexValidator('^\d{2}-\d{3}$', message="Nieprawidłowy kod pocztowy")


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, validators=[validate_password], label="Hasło")
    password2 = forms.CharField(widget=forms.PasswordInput, validators=[validate_password], label="Powtórz hasło")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "gender",
            "dob",
        ]

        help_texts = {
            "username": "",
        }

        labels = FORM_LABELS_PL

    def clean(self):
        cd = super().clean()
        pass1 = cd.get("password1")
        pass2 = cd.get("password2")
        if pass1 != pass2:
            raise ValidationError("Hasła nie pasują!")


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika")
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")

    def clean(self):
        cd = super().clean()
        username = cd.get("username")
        password = cd.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError("Nieprawidłowe dane logowania")


class UserProfileSettingsForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}), label="Nazwa użytkownika")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "gender",
            "dob",
            "bio",
            "photo",
            "phone",
        ]
        labels = FORM_LABELS_PL


class UserChangePasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    new_password2 = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])

    def clean(self):
        cd = super().clean()
        new_password = cd.get("new_password")
        new_password2 = cd.get("new_password2")
        if new_password != new_password2:
            raise ValidationError("Hasła nie są jednakowe!")


class UserAddressForm(forms.ModelForm):
    post_code = forms.CharField(max_length=6, validators=[POST_CODE_VALIDATOR_PL], label="Kod pocztowy")

    class Meta:
        model = Address
        fields = ["street", "city", "post_code"]
        labels = FORM_LABELS_PL


class MeetingAddForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = [
            "date",
            "time",
            "max_users",
            "max_dogs",
            "target_user_gender",
            "target_user_age",
            "target_dog_sex",
            "target_dog_age",
            "notes",
            "address",
            "participating_dogs",
        ]
