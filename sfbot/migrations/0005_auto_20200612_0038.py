# Generated by Django 3.1a1 on 2020-06-11 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfbot', '0004_auto_20200612_0030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bots',
            name='SF_Username',
        ),
        migrations.AddField(
            model_name='bots',
            name='username',
            field=models.CharField(max_length=40, null=True, verbose_name='SF Username'),
        ),
    ]
