from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset

from psinder.settings import DATE_INPUT_FORMATS
from .models import Address, Meeting, GENDERS

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
    "date": "Data",
    "time": "Godzina",
    "max_users": "Maks użytkowników",
    "max_dogs": "Maks psów",
    "target_user_gender": "Płeć użytkownika",
    "target_user_age": "Wiek użytkownika",
    "target_dog_sex": "Płeć psa",
    "target_dog_age": "Wiek psa",
    "notes": "Dodatkowe informacje",
    "address": "Adres",
    "participating_dogs": "Moje psy",
}

POST_CODE_VALIDATOR_PL = RegexValidator('^\d{2}-\d{3}$', message="Nieprawidłowy kod pocztowy")


class UserCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', "Zarejestruj"))

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', "Zaloguj"))

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', "Zapisz zmiany"))

    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDERS, label="Płeć")

    class Meta:
        model = User
        fields = [
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', "Zapisz hasło"))

    new_password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    new_password2 = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])

    def clean(self):
        cd = super().clean()
        new_password = cd.get("new_password")
        new_password2 = cd.get("new_password2")
        if new_password != new_password2:
            raise ValidationError("Hasła nie są jednakowe!")


class UserAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', "Zapisz adres"))

    post_code = forms.CharField(max_length=6, validators=[POST_CODE_VALIDATOR_PL], label="Kod pocztowy")

    class Meta:
        model = Address
        fields = ["street", "city", "post_code"]
        labels = FORM_LABELS_PL


class MeetingAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', "Zapisz spotkanie"))

    street = forms.CharField(min_length=3, max_length=64, required=False, label="Ulica")
    city = forms.CharField(min_length=2, max_length=30, required=True, label="Miasto")
    post_code = forms.CharField(max_length=6, validators=[POST_CODE_VALIDATOR_PL], label="Kod pocztowy", required=False)

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
            "participating_dogs",
        ]
        labels = FORM_LABELS_PL

        widgets = {
            "participating_dogs": forms.CheckboxSelectMultiple
        }


class MeetingSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', "Wyszukaj"))

    city = forms.CharField(max_length=30, label="Miasto")
    date = forms.DateField(widget=forms.DateInput(format=DATE_INPUT_FORMATS, attrs={
        "type": "date",
        "min": datetime.now().date(),
        "value": datetime.now().date(),
    }), label="Data")
    target_user_gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDERS,
                                           label="Płeć", help_text="Wybierz płeć osoby, z którą chcesz się spotkać")
    max_users = forms.IntegerField(widget=forms.NumberInput, label="Maksymalna liczba uczestników", required=False,
                                   validators=[MinValueValidator(2), MaxValueValidator(10)],
                                   help_text="Podaj wartość w zakresie od 2 do 10")
    max_dogs = forms.IntegerField(widget=forms.NumberInput, label="Maksymalna liczba psów", required=False,
                                  validators=[MinValueValidator(0), MaxValueValidator(10)],
                                  help_text="Podaj wartość w zakresie od 0 do 10")


class MeetingJoinForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', "Dołącz"))

    def clean(self):
        cd = super().clean()
        participating_dogs = cd.get("participating_dogs")
        max_dogs = cd.get("max_dogs")
        if participating_dogs is None:
            return
        if len(self.initial["participating_dogs"]) + len(participating_dogs) > max_dogs:
            raise ValidationError(f"Nie możesz zabrać tylu psów! Maksymalna liczba psów na spotkaniu to {max_dogs}")

    class Meta:
        model = Meeting
        fields = ["participating_dogs", "max_dogs", "max_users"]

        widgets = {
            "participating_dogs": forms.CheckboxSelectMultiple,
            "max_dogs": forms.HiddenInput,
            "max_users": forms.HiddenInput,
        }

        labels = FORM_LABELS_PL

        help_texts = {
            "participating_dogs": "Wybierz psy, które zabierzesz ze sobą"
        }


class SearchProfilesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', "Szukaj"))

    query = forms.CharField(widget=forms.TextInput, label="Szukaj", help_text="Szukaj profili użytkowników i piesków")
