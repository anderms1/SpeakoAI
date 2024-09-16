from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
LENGUAGE_LEVEL_CHOICES = [
        ('beginner', 'Principiante'),
        ('intermediate', 'Intermedio'),
        ('advanced', 'Avanzado'),
    ]

LENGUAGE_CHOICES =[
        ('es','Español'),
        ('en','English'),
        ('fr','Français'),
        ('de','Deutsch'),
        ('pt','Portugues'),
    ]

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    native_language = models.CharField(max_length=10, choices=LENGUAGE_CHOICES, default='es')
    register_date = models.DateField(auto_now_add=True)
    profile_photo = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class UserLanguage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lenguages')
    progress = models.FloatField(default=0)
    lenguage_level = models.CharField(max_length=20, choices=LENGUAGE_LEVEL_CHOICES, default='beginner')
    studying_lenguage = models.CharField(max_length=10, choices=LENGUAGE_CHOICES, default='en')

    def __str__(self):
        return f'{self.user.username} - Estudiando {self.get_studying_lenguage_display()}'
