# Generated by Django 3.1a1 on 2020-06-13 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfbot', '0009_plan_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active Registration')),
            ],
        ),
    ]
