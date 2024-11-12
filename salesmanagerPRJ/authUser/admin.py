from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

class AdminUser(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = User

    list_display = ['get_first_name','get_surname', 'phone_number', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']

    def get_first_name(self, object):
        return object.name.firstname
    
    def get_surname(self, object):
        return object.name.surname
    
    get_first_name.short_description = "First Name"
    get_surname.short_description = 'Surname'

    fieldsets = (
        (None, {'fields': ('phone_number','password')}),
        ('Personal Info', {'fields': ('first_name','last_name')}),
        ('Permissions',{'fields':('is_staff','is_active','is_superuser','groups','user_permissions','privileges')}),
        ('Important dates', {'fields': ('date_joined','last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes':('wide'),
            'fields': ('email','password1','password2', 'is_staff','is_active','privileges')
        }),
    )

    search_fields = ('phone_number',)
    ordering = ('privileges',)

    # Register your models here.
#admin.site.register(User, AdminUser)