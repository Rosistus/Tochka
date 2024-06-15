from django.contrib import admin
from users.models import User, TempBan, TempBanAdmin
# Register your models here.

admin.site.register(User)
admin.site.register(TempBan, TempBanAdmin)
