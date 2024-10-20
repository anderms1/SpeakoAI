# Generated by Django 5.0.1 on 2024-10-17 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_lenguage_level_userlanguage_language_level_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='native_language',
            field=models.CharField(choices=[('es', 'Español'), ('en-us', 'English')], default='es', max_length=10),
        ),
        migrations.AlterField(
            model_name='userlanguage',
            name='studying_language',
            field=models.CharField(choices=[('es', 'Español'), ('en-us', 'English')], default='en', max_length=10),
        ),
        migrations.AlterField(
            model_name='userlanguage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to=settings.AUTH_USER_MODEL),
        ),
    ]
