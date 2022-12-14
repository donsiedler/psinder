from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Dog, GENDERS, SIZES

FORM_LABELS_PL = {
    "name": "Imię",
    "age": "Wiek",
    "sex": "Płeć",
    "breed": "Rasa",
    "size": "Wielkość",
    "bio": "Opis profilu",
    "photo": "Zdjęcie profilowe",
}


class DogCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', "Dodaj psa"))

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


class DogProfileSettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', "Zapisz zmiany"))

    sex = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDERS, label="Płeć")
    size = forms.ChoiceField(widget=forms.RadioSelect, choices=SIZES, label="Wielkość")

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
