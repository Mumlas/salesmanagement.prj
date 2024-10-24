from django.conf import settings
from django.shortcuts import render
from .models import User

# Create your views here.
def login(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        login_valid = settings.ADMIN_LOGIN == username
        pwd_valid = settings.ADMIN_PASSWORD == password

        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                print('User not found')