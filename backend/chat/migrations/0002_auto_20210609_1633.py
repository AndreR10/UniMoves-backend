# Generated by Django 3.1.7 on 2021-06-09 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='landlord',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landlord_chat', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chat',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenant_chat', to=settings.AUTH_USER_MODEL),
        ),
    ]
