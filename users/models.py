from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin


# Create your models here.
class User(AbstractUser):
    blessed = models.BooleanField(null=True, blank=True, default=0)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username


class TempBan(models.Model):
    class Meta:
        db_table = "TempBan"

    ip_address = models.GenericIPAddressField("IP адрес")
    attempts = models.IntegerField("Неудачных попыток входа", default=0)
    time_unblock = models.DateTimeField("Время разблокировки", blank=True)

    def __str__(self):
        return self.ip_address


class TempBanAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'attempts', 'time_unblock')
    search_fields = ('ip_address',)
