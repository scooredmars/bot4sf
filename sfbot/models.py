from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class GeneratePage(models.Model):
    def __str__(self):
        return self


class FaqList(models.Model):
    topic = models.CharField(max_length=70)
    description = models.TextField()

    def __str__(self):
        return self.topic


class Bots(models.Model):
    STATUS = (
        ("ON", "ON"),
        ("OFF", "OFF"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    plan = models.ForeignKey("sfbot.Plan", on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=4, choices=STATUS, default="OFF")
    time_left = models.IntegerField(null=True)
    game_settings = models.OneToOneField(
        "sfbot.GameSettings", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.game_settings.ac_settings.ac_username

    class Meta:
        verbose_name = _("bots")
        verbose_name_plural = _("Bots")


class GameSettings(models.Model):
    STATUS = (
        ("ON", "ON"),
        ("OFF", "OFF"),
    )
    TAVERN = (
        ("Gold", "Gold"),
        ("Exp", "Exp"),
        ("Time", "Time"),
    )
    ARENA = (
        ("Stop fight after 10 wins", "Stop fight after 10 wins"),
        (
            "Attack opponents who have items for your cluster",
            "Attack opponents who have items for your cluster",
        ),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ac_settings = models.OneToOneField(
        "sfbot.AcSettings", on_delete=models.CASCADE, null=True
    )
    tavern_status = models.CharField(max_length=3, choices=STATUS, default="OFF")
    tavern_settings = models.CharField(max_length=4, choices=TAVERN, default="Exp")
    arena_status = models.CharField(max_length=3, choices=STATUS, default="OFF")
    arena_settings = models.CharField(
        max_length=50, choices=ARENA, default="Stop fight after 10 wins"
    )

    def __str__(self):
        return self.ac_settings.ac_username

    def get_absolute_url(self):
        return reverse("sfbot:settings", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = _("gamesettings")
        verbose_name_plural = _("Game Settings")


class AcSettings(models.Model):
    COUNTRY = (("Intercontinental", "Intercontinental"),)
    SERVER = (
        ("s1", "s1"),
        ("s2", "s2"),
        ("s3", "s3"),
        ("s4", "s4"),
        ("s5", "s5"),
    )
    ac_username = models.CharField(max_length=40)
    password = models.CharField(max_length=30)
    country = models.CharField(
        max_length=20, choices=COUNTRY, default="Intercontinental"
    )
    server = models.CharField(max_length=4, choices=SERVER)

    def __str__(self):
        return self.ac_username


class Plan(models.Model):
    NAME = (
        ("FOR BEGINNERS", "FOR BEGINNERS"),
        ("I DON'T HAVE TIME", "I DON'T HAVE TIME"),
        ("I'M ON VACATION", "I'M ON VACATION"),
    )
    name = models.CharField(max_length=21, choices=NAME, default="FOR BEGINNERS")
    price = models.IntegerField()
    description = models.CharField(max_length=70)
    permission_list = models.ManyToManyField("sfbot.PermissionList")
    special_style = models.CharField(max_length=15, null=True, blank=True)
    max_time = models.IntegerField()
    max_bots = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("plan")
        verbose_name_plural = _("plans")


class PermissionList(models.Model):
    NAME = (
        ("6h", "6h"),
        ("1bot", "1bot"),
        ("12h no", "12h no"),
        ("3bots no", "3bots no"),
        ("12h yes", "12h yes"),
        ("3bots yes", "3bots yes"),
        ("24h no", "24h no"),
        ("5bots no", "5bots no"),
        ("24h yes", "24h yes"),
        ("5bots yes", "5bots yes"),
    )
    ICON = (
        ("check icon", "check icon"),
        ("times icon", "times icon"),
    )
    DESCRIPTION = (
        ("Bot works 6h per day", "Bot works 6h per day"),
        ("Max 1 bot", "Max 1 bot"),
        ("Bot works 12h per day", "Bot works 12h per day"),
        ("Max 3 bots", "Max 3 bots"),
        ("Bot works all the time", "Bot works all the time"),
        ("Max 5 bot", "Max 5 bot"),
    )
    name = models.CharField(max_length=40, choices=NAME)
    icon = models.CharField(max_length=40, choices=ICON)
    description = models.CharField(max_length=40, choices=DESCRIPTION)

    def __str__(self):
        return self.name
