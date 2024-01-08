# Generated by Django 5.0.1 on 2024-01-07 13:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0009_mailingoptions_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='owner',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
