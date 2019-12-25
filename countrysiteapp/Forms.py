import django
from django import forms

from .models import login


class loginForm(django.forms.ModelForm):
    class Meta:
        model = login
        fields = ['first_name','last_name','phone','Gender']
