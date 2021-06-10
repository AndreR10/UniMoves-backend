# Generated by Django 3.1.7 on 2021-06-09 16:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('viewedLandlord', models.BooleanField(default=False)),
                ('viewedTenant', models.BooleanField(default=False)),
            ],
        ),
    ]
