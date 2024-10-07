from django.contrib import admin
from .models import UserTable, LoginTable

# Register your models here.
admin.site.register(UserTable)
admin.site.register(LoginTable)