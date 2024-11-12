from django.db import models
from setup.models import Staff
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


# Create your models here.

class Privileges(models.TextChoices):
    PUMP_ATTENDANT = 'pump_attendant'
    SUPERVISOR = 'supervisor'
    MANAGER = 'manager'
    CASHIER = 'cashier_accountant'
    MD_CEO = 'md_ceo'
    DRIVER = 'driver'
    ADMIN = "system_admin"
    OTHERS = "Others"

# User table
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=11, unique=True)
    password = models.CharField(max_length=100)
    staff = models.ForeignKey(Staff, related_name='user_staff', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True)
    role = models.CharField(verbose_name='Role',max_length=100, choices=zip(Privileges,Privileges))

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS=[]

    objects = CustomUserManager()

    def __str__(self):
        return self.staff.firstname
    
    class Meta:
        verbose_name_plural="Users"