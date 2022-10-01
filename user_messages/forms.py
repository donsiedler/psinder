from django import forms


class ThreadCreateForm(forms.Form):
    username = forms.CharField(max_length=150, label="")
