from django.db import models
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


class PermissionList(models.Model):
    name = models.CharField(max_length=40)
    icon = models.CharField(max_length=40)
    description = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Plan(models.Model):
    NAME = (
        ("FOR BEGINNERS", "FOR BEGINNERS"),
        ("I DON'T HAVE TIME", "I DON'T HAVE TIME"),
        ("I'M ON VACATION", "I'M ON VACATION"),
    )
    name = models.CharField(max_length=21, choices=NAME, default="FOR BEGINNERS")
    price = models.IntegerField()
    description = models.CharField(max_length=70)
    permission_list = models.ManyToManyField(PermissionList)
    special_style = models.CharField(max_length=15, null=True, blank=True)
    max_time = models.IntegerField()
    max_bots = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("plan")
        verbose_name_plural = _("plans")
