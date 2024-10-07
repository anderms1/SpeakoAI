from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from django.http import JsonResponse

# Create your views here.
@login_required
def dashboard_view(request):
    return render(request, 'core/dashboard.html')

@login_required
def profile_view(request):
    return render(request, 'core/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        try:
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()

            response_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
            }

        except CustomUser.DoesNotExist:
            response_data = {'error': 'Datos del usuario no encontrados'}

        return JsonResponse(response_data)

def translator_view(request):
    return render(request, 'core/translator.html')

def chat_view(request):
    return render(request, 'core/chat.html')