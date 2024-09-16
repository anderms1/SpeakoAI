from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, UserLanguageForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, request.FILES)
        language_form = UserLanguageForm(request.POST)
        if user_form.is_valid() and language_form.is_valid():
            user = user_form.save()
            language = language_form.save(commit=False)
            language.user = user
            login(request, user)
            return redirect('home')
    else:
        user_form = CustomUserCreationForm()
        language_form = UserLanguageForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'language_form': 'language_form'
        })


def layout(request):
    return render(request, 'users/layout.html')