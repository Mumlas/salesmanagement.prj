from django.shortcuts import render
from django.views import View

# Create your views here.


class RegistrationView(View):
    def get(self, request):
        return render(request,'authentication/register.html')
    
def register(request):
    return render(request,'authentication/register.html')

def login(request):
    return render(request,'authentication/login.html')

def newPassword(request):
    return render(request,'authentication/new_password.html')

def resetPassword(request):
    return render(request,'authentication/reset_password.html')

