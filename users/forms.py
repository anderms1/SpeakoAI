from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserLanguage


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'native_language', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'rounded-md w-full'})
        self.fields['last_name'].widget.attrs.update({'class': 'rounded-md w-full'})
        self.fields['email'].widget.attrs.update({'class': 'rounded-md w-full'})
        self.fields['native_language'].widget.attrs.update({'class': 'rounded-md w-full'})
        self.fields['password1'].widget.attrs.update({'class': 'rounded-md w-full'})
        self.fields['password2'].widget.attrs.update({'class': 'rounded-md w-full'})

class UserLanguageForm(forms.ModelForm):
    class Meta:
        model = UserLanguage
        fields = ['studying_language', 'language_level']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['studying_language'].widget.attrs.update({'class': 'rounded-md w-full'})
        self.fields['language_level'].widget.attrs.update({'class': 'rounded-md w-full'})


class EmailAuthenticationForm(forms.Form):
    username = forms.EmailField(label='Email',max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Email o contraseña incorrectos.")
        return self.cleaned_data
    
    def get_user(self):
        return self.user_cache
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'rounded-md w-full'})
        self.fields['password'].widget.attrs.update({'class': 'rounded-md w-full'})