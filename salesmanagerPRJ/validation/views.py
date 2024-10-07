from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User # build user model TOBE CHANGED LATER
from validate_email import validate_email
from django.contrib import messages


# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        email=data['email']

        if not validate_email(email):
            return JsonResponse({'email_error':'invalid email'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'sorry email in use, choose another email'}, status=409)
        
        return JsonResponse({'email_valid':True})    


class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric character'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'sorry username in use, choose another username'}, status=409)
        
        return JsonResponse({'username_valid':True})
    


    
class RegistrationView(View):
    def get(self, request):
        return render(request,'authentication/register.html')
    
    def post(self, request):

        # get user data
        # validate
        # create a user account

        firstname = request.POST['fname']
        surname = request.POST['sname']
        phone = request.POST['phone']
        email = request.POST['email']
        designation = request.POST['designation']
        branch = request.POST['branch']
        dateofbirth = request.POST['dateofbirth']
        employmentdate = request.POST['employmentdate']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if not User.objects.filter(phone=phone).exists():

                    if len(password) < 6:
                        messages.error(request, "Passowrd too short")
                        return render(request,"authentiation/register.html")
                    
                    if password != password1:
                        messages.error(request, "authentication/register.html")
                    
                    user = User.objects.create_user(
                        firstname=firstname,
                        surname=surname,
                        phone=phone,
                        email=email,
                        branch=branch,
                        designation=designation,
                        dateofbirth=dateofbirth,
                        employmentdate=employmentdate,
                        username=username
                    )
                    user.set_password(password)
                    user.save()

                    messages.error(request, "User Successfully created") 
                    return render(request,"authentiation/register.html")

        return render(request,'authentication/register.html')
    
def register(request):
    return render(request,'authentication/register.html')

def login(request):
    return render(request,'authentication/login.html')

def newPassword(request):
    return render(request,'authentication/new_password.html')

def resetPassword(request):
    return render(request,'authentication/reset_password.html')

