from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from setup.models import Staff

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        privileges ='Others'
        if not username:
            raise ValueError(_("The phonenumber must be set"))
                
        staff = Staff.objects.get(phonenumber=username)

        #email = self.normalize_email(email)
        user = self.model(username=username, staff=staff, **extra_fields)
        user.set_password(password)
        print(f'User detail: {user}')
        print(f'User details: {username} {staff} {privileges}')
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault("privileges",'Others')

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        if extra_fields.get("is_admin") is not True:
            raise ValueError(_("Superuser must have is_admin=True."))
        if extra_fields.get("is_active") is not True:
            raise ValueError(_("Superuser must have is_active=True."))
        return self.create_user(username, password, **extra_fields)

