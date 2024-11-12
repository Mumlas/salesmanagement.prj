import json
from django.db import IntegrityError
from django.views import View
from .models import CustomUser
from setup.models import Staff
from sales.models import Shift
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from validate_email import validate_email
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout

# User model from settings
User = settings.AUTH_USER_MODEL
UserModel = get_user_model()


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

@login_required
def set_password(raw_password):
    password = make_password(raw_password)
    return password

class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric character'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'sorry username in use, choose another username'}, status=409)
        
        return JsonResponse({'username_valid':True})
    

@login_required
def get_staff(request, staff_id):
    print(staff_id)
    try:
        staff_id = int(staff_id)
        staff = Staff.objects.get(id=staff_id)
        print(f'Selected staff: {staff}')
        data = {
            "phonenumber":staff.phonenumber,
            "staff_id":staff.id,
            'role':staff.designation
        }
        print(data)
        return JsonResponse(data, safe=False)
    except Staff.DoesNotExist:
        print('Error')
        return JsonResponse({'error':'Staff member doesnot exist'}, status =404)

@login_required
def create_user(request):
    staff = Staff.objects.all()
    context = {
        'staff':staff,
    }

    if request.method=="POST":
        password = request.POST['password']
        if not password:
            messages.error(request, 'Password field can not be empty')
            return render(request,'authentication/register.html', context)
        if len(password) < 8:
            messages.error(request, 'Password is too short, password can not be less than 8 characters')
            return render(request,'authentication/register.html', context)
        
        password1 = request.POST['password1']
        if (password != password1):
            messages.error(request, 'Password and confirm password fields are not thesame')
            return render(request,'authentication/register.html', context)
        
        role = request.POST['role']
        if not role:
            messages.error(request, 'Assign role to the user')
            return render(request,'authentication/register.html', context)
        
        staff_id = request.POST['staff']
        if not staff_id:
            messages.error(request, 'Select staff to profile')
            return render(request,'authentication/register.html', context)
        
        staff = Staff.objects.get(id=int(staff_id))

        username = request.POST['username']
        if not username:
            messages.error(request, 'Phone number field can not be empty')
            return render(request,'authentication/register.html', context)

        try:
            new_user = CustomUser.objects.create_user(
                username = username,
                role = role,
                password = password,
                is_active=True
            )

            new_user.staff = staff

            new_user.save()

            print(f'User: {username} created')

            messages.success(request, f'User: {staff} with username - {username} is profiled.')
            return render(request,'authentication/register.html', context)
        
        except AttributeError:
            messages.error(request, f'User can not be created ensure the entries are correct')
            return render(request,'authentication/register.html', context)

        except IntegrityError:
            messages.error(request, f'Username {staff} - {username} already exist')
            return render(request,'authentication/register.html', context)
            
    return render(request,'authentication/register.html', context)
        

    
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

@login_required
def register(request):
    return render(request,'authentication/register.html')

def login_user(request):

    if request.user.is_authenticated:
        messages.info(request,"You are already logged in")
        user = request.user
        staff = Staff.objects.get(id=user.staff.id)
        return redirect('shift-history', staff_id=staff.id)
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = UserModel.objects.get(username=username)
        except:
            messages.warning(request,f'User with username {username} does not exist')
            return render(request,'authentication/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'You are logged in')
            return redirect('main-dashboard')
        else:
            messages.warning(request,'User does not exist contact your supervisor')
            return render(request,"authentication/login.html")
    
    return render(request, 'authentication/login.html')

@login_required
def newPassword(request):
    return render(request,'authentication/new_password.html')

@login_required
def resetPassword(request):
    return render(request,'authentication/reset_password.html')

@login_required
def logout_user(request):
    messages.success(request,"You have succesfully logged out")
    logout(request)
    return render(request, 'authentication/logout.html')

@login_required
def profile_view(request):
    return render(request, 'authentication/profile.htm')