# Generated by Django 3.1 on 2020-09-18 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sfbot', '0003_auto_20200830_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='name',
            field=models.CharField(choices=[('STARTER', 'STARTER'), ('STANDARD', 'STANDARD'), ('PREMIUM', 'PREMIUM')], default='STARTER', max_length=21),
        ),
    ]
