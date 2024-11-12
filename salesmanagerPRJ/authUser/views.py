from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
#from .models import User
from .forms import CustomUserCreationForm
from setup.models import Staff

def get_staff(request, staff_id):
    try:
        staff = Staff.objects.get(id=staff_id)
        data = {
            "email":staff.email,
            "phone_number":staff.phonenumber
        }
        print(data)
        return JsonResponse(data, safe=False)
    except Staff.DoesNotExist:
        return JsonResponse({'error':'Staff member doesnot exist'}, status =404)

#create user
def create_user(request):
    form = CustomUserCreationForm()

    if request.method=="POST":
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            messages.error(request, "Password and Confirm password aren't same")
            return render(request, 'authUser/register.html', {"form":form})
         
        privileges = request.POST.get('privileges')
        if not privileges:
            messages.error(request, 'Assign role to the user')
            return render(request, 'authUser/register.html', {"form":form})

        User.objects.create(
            phone_number=phone_number,
            password=password,
            privileges=privileges
        )        
        messages.error(request, 'Assign role to the user')
        return render(request, 'authUser/register.html', {'form':form})
    else:
        return render(request, 'authUser/register.html', {'form':form})

def reset_password(request):
    pass

def new_password(request):
    pass

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

def logout(request):
    pass