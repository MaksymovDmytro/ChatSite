from django import forms
from .models import Thread


class ComposeForm(forms.Form):
    message = forms.CharField(
            widget=forms.TextInput(
                attrs={"class": "form-control"}
                )
            )
