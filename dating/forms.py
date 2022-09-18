from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


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

        labels = {
            "username": "Nazwa użytkownika",
            "email": "Adres email",
            "first_name": "Imię",
            "last_name": "Nazwisko",
            "gender": "Płeć",
            "dob": "Data urodzenia",
        }

    def clean(self):
        cd = super().clean()
        pass1 = cd.get("password1")
        pass2 = cd.get("password2")
        if pass1 != pass2:
            raise ValidationError("Hasła nie pasują!")
