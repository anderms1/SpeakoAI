from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
import json
from django.http import JsonResponse
from .services import translate_deepl
import openai
from .models import ChatMessage
from django.shortcuts import redirect
from django.contrib.auth import logout

import os
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    messages = ChatMessage.objects.filter(user=request.user).order_by("timestamp")
    return render(request, 'core/chat.html', {'messages': messages})

@login_required
def chat_api_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get("message")
            user = request.user

            name = user.first_name
            user_language = user.languages.first()
            level = user_language.language_level
            language = user_language.studying_language

            messages = ChatMessage.objects.filter(user=user).order_by("timestamp")
            conversation = [{"role": "system", "content": f"You are an {language} teacher helping the user learn {language}."},
                            {"role": "system", "content": f"The user's name is {name}."},
                            {"role": "system", "content": f"Your name is Quik"},
                            {"role": "system", "content": f"Pay attention to their messages in {language}, if there is a mistake, correct it first."},
                            {"role": "system", "content": f"Speak in {language} with the user, unless the user tell to speak in her language."},
                            {"role": "system", "content": f"The user has an {level} level of English."},
                            {"role": "system", "content": "Focus on improving their vocabulary and grammar."}]
            for msg in messages:
                conversation.append({"role": msg.role, "content": msg.content})

            conversation.append({"role": "user", "content": user_message})

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=conversation
            )

            assistant_message = response["choices"][0]["message"]["content"]

            ChatMessage.objects.create(user=user, role="user", content=user_message)
            ChatMessage.objects.create(user=user, role="assistant", content=assistant_message)

            return JsonResponse({"response": assistant_message})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)    
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    

def logout_view(request):
    logout(request)
    return redirect('/')