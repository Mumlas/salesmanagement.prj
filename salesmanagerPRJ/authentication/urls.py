from . import views
from django.urls import path
from .views import RegistrationView

urlpatterns = [
    path('register_cls', RegistrationView.as_view(), name='register_cls'),  
    #path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('reset_password', views.resetPassword, name='reset_password'),
    path('new_password', views.newPassword, name='new_password'),
]

