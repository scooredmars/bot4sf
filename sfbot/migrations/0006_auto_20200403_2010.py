# Generated by Django 3.0.4 on 2020-04-03 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfbot', '0005_auto_20200403_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='permission_list',
            field=models.ManyToManyField(to='sfbot.PermissionList'),
        ),
    ]