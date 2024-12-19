from . import views
from django.urls import path
from .views import RegistrationView, UsernameValidationView, EmailValidationView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register_cls/', RegistrationView.as_view(), name='register_cls'),  
    path('', views.login_user, name='login_user'),
    path('reset_password/', views.resetPassword, name='reset_password'),
    path('new_password/', views.newPassword, name='new_password'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), 
         name='validate-username'),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('register/get-staff/<int:staff_id>/', views.get_staff, name='get_staff'),
    path('register/', views.create_user, name='create_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('profile/', views.profile_view, name='profile'),

]