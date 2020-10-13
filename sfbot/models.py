from django.contrib.auth.models import AbstractBaseUser
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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    plan = models.ForeignKey("sfbot.Plan", on_delete=models.CASCADE, null=True)
    wallet = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.user.username


class Currency(models.Model):
    price = models.IntegerField(null=True)
    value = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = "Currency"

    def __str__(self):
        return str(self.value)


class Orders(models.Model):
    profile = models.ForeignKey(
        "sfbot.Profile", on_delete=models.CASCADE, null=True)
    order_create = models.DateTimeField(auto_now=True, null=True)
    currency_package = models.ForeignKey(
        "sfbot.Currency", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = "Orders"


class Plan(models.Model):
    NAME = (
        ("STARTER", "STARTER"),
        ("STANDARD", "STANDARD"),
        ("PREMIUM", "PREMIUM"),
    )
    name = models.CharField(max_length=21, choices=NAME, default="STARTER")
    price = models.IntegerField()
    permission_list = models.ManyToManyField("sfbot.PermissionList")
    special_style = models.CharField(max_length=15, null=True, blank=True)
    max_time = models.FloatField(null=True)
    max_bots = models.IntegerField(null=True)
    available = models.BooleanField(
        verbose_name="Plan is available", default=True)

    def __str__(self):
        return self.name


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


class Bots(AbstractBaseUser):
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
    COUNTRY = (("Intercontinental", "Intercontinental"),)
    SERVER = (
        ("s1", "s1"),
        ("s2", "s2"),
        ("s3", "s3"),
        ("s4", "s4"),
        ("s5", "s5"),
    )
    profile = models.ForeignKey(
        "sfbot.Profile", on_delete=models.CASCADE, null=True)
    status = models.BooleanField(verbose_name="Bot status", default=False)
    time_left = models.TimeField(null=True)
    converted_time = models.FloatField(null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    stop = models.DateTimeField(null=True, blank=True)

    username = models.CharField(
        verbose_name="SF Username", max_length=40, null=True)
    password = models.CharField(
        verbose_name="SF Password", max_length=30, null=True)
    country = models.CharField(
        max_length=20, choices=COUNTRY, default="Intercontinental", null=True
    )
    server = models.CharField(max_length=4, choices=SERVER, null=True)

    tavern_status = models.BooleanField(
        verbose_name="Tavern status", default=False)
    tavern_settings = models.CharField(
        max_length=4, choices=TAVERN, default="Exp")
    arena_status = models.BooleanField(
        verbose_name="Arena status", default=False)
    arena_settings = models.CharField(
        max_length=50, choices=ARENA, default="Stop fight after 10 wins"
    )

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("bots")
        verbose_name_plural = _("Bots")

    def get_absolute_url(self):
        return reverse("sfbot:settings", kwargs={"pk": self.pk})
