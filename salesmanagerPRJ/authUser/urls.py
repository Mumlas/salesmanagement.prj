from django.urls import path
from . import views

urlpatterns = [
    path('get-staff/<int:staff_id>/', views.get_staff, name='get_staff'),
    path('create-user/', views.create_user, name='create_user'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('new-password/', views.new_password, name='new_password'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]

