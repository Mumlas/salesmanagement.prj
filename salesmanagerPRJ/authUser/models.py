import re
from setup.models import Staff
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.

class CustomerUserManager(UserManager):
    def _create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Provide a valid phone number")
        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.setdefault('is_staff') is not True:
            raise ValueError(_('Super user must have "is_staff" set to True'))
        
        if extra_fields.setdefault('is_superuser') is not True:
            raise ValueError(_('Super user must have "is_superuser" set to True'))
        
        return self._create_user(phone_number, password, **extra_fields)

class Privileges(models.TextChoices):
    PUMP_ATTENDANT = 'pump_attendant'
    SUPERVISOR = 'supervisor'
    MANAGER = 'manager'
    CASHIER = 'cashier'
    MD_CEO = 'md_ceo'
    DRIVER = 'driver'

def validate_phone(value):
    phone_regex = re.compile(r'^\+?0?\d{10}$')
    if not phone_regex.match(value):
        raise ValueError(_('Invalid phone number.'))
    
class User(AbstractBaseUser,PermissionsMixin):
    phone_number = models.CharField(_('phone number'), validators=[validate_phone], max_length=11, unique=True, null=False)
    email = models.CharField(max_length=255, default='',null=True, unique=True)
    name = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='user_staff', null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    privileges = models.CharField(max_length=50, choices=Privileges.choices)

    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomerUserManager()

    USERNAME_FIELD ='phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = 'Users'

    def _str__(self):
        return self.phone_number
    
    @property
    def first_name(self):
        return self.name.firstname
    
    @property
    def last_name(self):
        return self.name.surname
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]