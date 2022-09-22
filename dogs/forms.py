from django import forms

from .models import Dog

FORM_LABELS_PL = {
    "name": "Imię",
    "age": "Wiek",
    "sex": "Płeć",
    "breed": "Rasa",
    "size": "Wielkość",
    "bio": "Opis profilu",
    "photo": "Zdjęcie profilowe",
}


class DogProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = [
            "name",
            "age",
            "sex",
            "breed",
            "size",
            "bio",
            "photo",
        ]
        labels = FORM_LABELS_PL
