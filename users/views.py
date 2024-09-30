from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, UserLanguageForm, EmailAuthenticationForm

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        language_form = UserLanguageForm(request.POST)
        if user_form.is_valid() and language_form.is_valid():
            user = user_form.save()
            language = language_form.save(commit=False)
            language.user = user
            language.progress = 0 
            language.save()
            login(request, user)
            return redirect('dashboard')
        else:
            # Mostrar los errores en la consola si algo falla
            print(user_form.errors)
            print(language_form.errors)
    else:
        user_form = CustomUserCreationForm()
        language_form = UserLanguageForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'language_form': language_form
        })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username'] 
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Email o contraseña incorrectos.")
    else:
        form = EmailAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def layout(request):
    return render(request, 'users/layout.html')

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'users/index.html')