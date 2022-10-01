from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class ThreadCreateForm(forms.Form):
    username = forms.CharField(max_length=150, label="")


class MessageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', "Wyślij", css_class="btn btn-psinder"))

    message = forms.CharField(widget=forms.TextInput(), label="")
