from django.db import models
from setup.models import Staff

# Create your models here.

# User table
class UserTable(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=520)
    staff = models.ForeignKey(Staff, related_name='username', on_delete=models.CASCADE)
    enable = models.BooleanField(default=False)
    password_count = models.DecimalField(max_digits=2, decimal_places=0, default=0)

    class Meta:
        verbose_name_plural="UserTable"

#Login Table
class LoginTable(models.Model):
    username = models.ForeignKey(UserTable, related_name='loggedin', on_delete=models.CASCADE)
    is_Active = models.BooleanField(default=False)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="LoginTable"