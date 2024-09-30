from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard_view(request):
    return render(request, 'core/dashboard.html')

@login_required
def profile_view(request):
    return render(request, 'core/profile.html')

def translator_view(request):
    return render(request, 'core/translator.html')

def chat_view(request):
    return render(request, 'core/chat.html')