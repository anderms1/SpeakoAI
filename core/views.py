from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
import json
from django.http import JsonResponse
from .services import translate_deepl

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
    
@login_required
def translator_view(request):
    return render(request, 'core/translator.html')

@login_required

def translate_api_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text')
            source_lang = data.get('source')
            target_lang = data.get('target')

            if(not text or not source_lang or not target_lang):
                return JsonResponse({'error': 'Faltan parámetros.'}, status=400)
            
            translated_text = translate_deepl(text, source_lang, target_lang)

            if translated_text:
                return JsonResponse({'translated_text': translated_text})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
def chat_view(request):
    return render(request, 'core/chat.html')
