from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserLanguage


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'native_language', 'password1', 'password2', 'profile_photo']

class UserLanguageForm(forms.ModelForm):
    class Meta:
        model = UserLanguage
        fields = ['studying_lenguage', 'lenguage_level', 'progress']