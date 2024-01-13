# Generated by Django 5.0.1 on 2024-01-10 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0018_alter_logs_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingoptions',
            name='send_period',
            field=models.CharField(choices=[(None, 'Выберите периодичность рассылки'), ('Ежеминутно', 'Ежеминутно'), ('Ежедневно', 'Ежедневно'), ('Еженедельно', 'Еженедельно'), ('Ежемесячно', 'Ежемесячно')], max_length=20, verbose_name='Периодичность'),
        ),
    ]
