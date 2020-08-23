# Generated by Django 3.1a1 on 2020-08-19 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FaqList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=70)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='GeneratePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PermissionList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('6h', '6h'), ('1bot', '1bot'), ('12h no', '12h no'), ('3bots no', '3bots no'), ('12h yes', '12h yes'), ('3bots yes', '3bots yes'), ('24h no', '24h no'), ('5bots no', '5bots no'), ('24h yes', '24h yes'), ('5bots yes', '5bots yes')], max_length=40)),
                ('icon', models.CharField(choices=[('check icon', 'check icon'), ('times icon', 'times icon')], max_length=40)),
                ('description', models.CharField(choices=[('Bot works 6h per day', 'Bot works 6h per day'), ('Max 1 bot', 'Max 1 bot'), ('Bot works 12h per day', 'Bot works 12h per day'), ('Max 3 bots', 'Max 3 bots'), ('Bot works all the time', 'Bot works all the time'), ('Max 5 bot', 'Max 5 bot')], max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('FOR BEGINNERS', 'FOR BEGINNERS'), ("I DON'T HAVE TIME", "I DON'T HAVE TIME"), ("I'M ON VACATION", "I'M ON VACATION")], default='FOR BEGINNERS', max_length=21)),
                ('price', models.IntegerField()),
                ('description', models.CharField(max_length=70)),
                ('special_style', models.CharField(blank=True, max_length=15, null=True)),
                ('max_time', models.FloatField(null=True)),
                ('max_bots', models.IntegerField(null=True)),
                ('available', models.BooleanField(default=True, verbose_name='Plan is available')),
                ('permission_list', models.ManyToManyField(to='sfbot.PermissionList')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sfbot.plan')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('status', models.BooleanField(default=False, verbose_name='Bot status')),
                ('time_left', models.TimeField(null=True)),
                ('converted_time', models.FloatField(null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('stop', models.DateTimeField(blank=True, null=True)),
                ('username', models.CharField(max_length=40, null=True, verbose_name='SF Username')),
                ('password', models.CharField(max_length=30, null=True, verbose_name='SF Password')),
                ('country', models.CharField(choices=[('Intercontinental', 'Intercontinental')], default='Intercontinental', max_length=20, null=True)),
                ('server', models.CharField(choices=[('s1', 's1'), ('s2', 's2'), ('s3', 's3'), ('s4', 's4'), ('s5', 's5')], max_length=4, null=True)),
                ('tavern_status', models.BooleanField(default=False, verbose_name='Tavern status')),
                ('tavern_settings', models.CharField(choices=[('Gold', 'Gold'), ('Exp', 'Exp'), ('Time', 'Time')], default='Exp', max_length=4)),
                ('arena_status', models.BooleanField(default=False, verbose_name='Arena status')),
                ('arena_settings', models.CharField(choices=[('Stop fight after 10 wins', 'Stop fight after 10 wins'), ('Attack opponents who have items for your cluster', 'Attack opponents who have items for your cluster')], default='Stop fight after 10 wins', max_length=50)),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sfbot.profile')),
            ],
            options={
                'verbose_name': 'bots',
                'verbose_name_plural': 'Bots',
            },
        ),
    ]
