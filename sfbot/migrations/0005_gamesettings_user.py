# Generated by Django 3.0.4 on 2020-05-01 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sfbot', '0004_auto_20200501_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamesettings',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
