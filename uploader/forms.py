"""

"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FileUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'bt-select'}),
    )

class SignUpForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'password')

