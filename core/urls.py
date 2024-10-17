from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('translator/', views.translator_view, name='translator'),
    path('chat/', views.chat_view, name='chat'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('translate-api/', views.translate_api_view, name='translate_api'),
]
