from django.contrib import admin


# Register your models here.
from .models import ClientList, User, UserManager

admin.site.register(ClientList)
admin.site.register(User)
