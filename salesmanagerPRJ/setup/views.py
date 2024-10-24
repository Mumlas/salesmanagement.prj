from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import *
from datetime import date, datetime


# Create your views here.

class BranchView(View):
    def get(self, request):
        return render(request,'setup/branch.html')
    
    def post(self, request):
        # NewBranch = Branch()
        context = {
            'name':request.POST,
            'address':request.POST
        }
        if request.method=="POST":
            branch = request.POST['branchName']
            if not branch:
                messages.error(request, 'Provide the branch name')
                return render(request, 'setup/branch.html')
    
            address = request.POST['branchAddress']
            if not address:
                messages.error(request, 'Provide the branch address')
                return render(request, 'setup/branch.html')
        
            Branch.objects.create(branchName = branch,
                      branchAddress = address)
            #Branch.save()
            messages.success(request, 'Branch added successfully')
            return redirect('branch')
    

class ProductView(View):
    def get(self, request):
        return render(request,'setup/product.html')
    
    def post(self, request):

        if request.method=="POST":
            productName = request.POST.get('productName')
            if not productName:
                messages.error(request, 'Enter the Product Name supplied')
                return render(request, 'setup/product.html')
            
            productDescription = request.POST.get('productDescription')
            
            Product.objects.create(productName=productName,
                                   productDescription=productDescription)
            messages.success(request, 'Product Added successfully')
            return render(request,'setup/product.html')    
              
    
class PumpView(View):
    def get(self, request):
        facilities = Storage.objects.all()
        context = {
            'facilities':facilities,
            'values':request.POST
        }
        return render(request,'setup/pump.html', context)
    
    def post(self, request):
        facilities = Storage.objects.all()

        context = {
            'facilities':facilities,
            'values':request.POST
        }

        if request.method == "POST":
            pumpDescription = request.POST.get('pumpDescription')
            if not pumpDescription:
                messages.error(request, 'Provide the Name/Description')
                return render(request, 'setup/pump.html', {'facilities':facilities})  

            facility = request.POST.get('facility')
            if not facility:
                messages.error(request, 'Select the storage/Tank')
                return render(request, 'setup/pump.html', {'facilities':facilities})  
            try:
                facility_id = int(facility)
                facility = Storage.objects.get(id=facility_id)
            except Storage.DoesNotExist:
                return render(request, "setup/pump.html", {
                    'facilities':facilities,
                    'error':'Selected Storage facility does not exist.'
                })
            
            Pump.objects.create(pupmDesc=pumpDescription,
                                storage = facility)
            messages.success(request, 'Pump added successfully')
            return render(request,'setup/pump.html', {'facilities':facilities})  
                    

class ShiftView(View):
    def get(self, request):
        return render(request,'setup/shift.html')
    
class StorageView(View):
    def get(self,request):
        branches = Branch.objects.all()
        products = Product.objects.all()


        context = {
            'branches' : branches,
            'products' : products,
            'values' : request.POST
        }  

        return render(request,'setup/storage.html', context)

    #@login_required(login_url='validation/login')       
    def post(self,request):
        branches = Branch.objects.all()
        products = Product.objects.all()
        context = {
            'branches' : branches,
            'products' : products,
            'values' : request.POST
        } 

        if request.method == 'POST':
            storage = request.POST.get('storage')
            if not storage:
                messages.error(request, 'Provide the Name/Description')
                return render(request, 'setup/storage.html', context)

            branchID = int(request.POST.get('branch'))
            if not branchID:
                messages.error(request, 'Select the branch where the facility is located')
                return render(request, 'setup/storage.html', context)

            productID = int(request.POST.get('product'))
            if not productID:
                messages.error(request, 'Select the product')
                return render(request, 'setup/storage.html', context)
                                  
            quantity = request.POST.get('quantity')
            if not quantity:
                messages.error(request, 'Enter the capacity of the storage facility')
                return render(request, 'setup/storage.html', context)
            
            try:
                branch_id = int(branchID)
                branch = Branch.objects.get(id=branch_id)
            except Branch.DoesNotExist:
                return render(request, "setup/storage.html", {
                    'branches':branches,
                    'error':'Selected branch does not exist.'
                })

            try:
                product_id = int(productID)
                product = Product.objects.get(id=product_id)
            except Branch.DoesNotExist:
                return render(request, "setup/storage.html", {
                    'products':products,
                    'error':'Selected product does not exist.'
                })
      
            Storage.objects.create(storageDesc = storage,
                                   capacity = quantity,
                                   branch = branch,
                                   product=product)

            messages.success(request, 'Storage Facility added successfully')
            return render(request,'setup/storage.html', context)    

class StaffView(View):
    def get(self, request):
        branches = Branch.objects.all()
        context = {
            "branches":branches
        }
        return render(request,'setup/staff.html', context)
    
    def post(self, request):

        branches = Branch.objects.all()
        context = {
            "branches":branches
        }
    
        if request.method=="POST":
            title = request.POST.get('title')
            if not title:
                messages.error(request,'Invalid input, select a valid TITLE')
                return render(request,'setup/staff.html', context)

            firstname = request.POST.get('fname')
            if not firstname:
                messages.error(request,'Invalid FIRST NAME, enter a valid FIRST NAME')
                return render(request,'setup/staff.html', context)
            if len(str(firstname)) < 3 | len(str(firstname)) >50:
                messages.error(request,'FIRST NAME too short or too long, enter FIRST NAME between 3 to 50 characters')
                return render(request,'setup/staff.html', context)
            
            surname = request.POST.get('sname')
            if not surname:
                messages.error(request,'Invalid SURNAME, enter a valid SURNAME')
                return render(request,'setup/staff.html', context)
            if  len(str(surname)) < 3 | len(str(surname))>50:
                messages.error(request,'SURNAME too short or too long, enter SURNAME between 3 to 50 characters')
                return render(request,'setup/staff.html', context)
            
            sex = request.POST.get('sex')
            if not sex:
                messages.error(request,'Invalid input, select a valid sex')
                return render(request,'setup/staff.html', context)            

            dateofbirth = request.POST.get('dateofbirth')
            if not dateofbirth:
                messages.error(request,'Select a valid date of birth')
                return render(request,'setup/staff.html', context)

            try:
                dateofbirth = datetime.strptime(dateofbirth, '%Y-%m-%d').date()
                print(dateofbirth.year)
                if date.today().year - dateofbirth.year < 18:
                    messages.error(request,'Staff can not be younger than 18 years old')
                    return render(request,'setup/staff.html', context)
            except ValueError:
                    messages.error(request,'Not a valid date of birth')
                    return render(request,'setup/staff.html', context)
                            
            employmentdate = request.POST.get('employmentdate')

            if not employmentdate:
                messages.error(request,'Select a valid date of employment')
                return render(request,'setup/staff.html', context)
            
            try:
                employmentdate = datetime.strptime(employmentdate, '%Y-%m-%d').date()
                if  employmentdate > date.today():
                    messages.error(request,'In consistent date of employment')
                    return render(request,'setup/staff.html', context)
            except ValueError:
                    messages.error(request,'Not a valid date of employment')
                    return render(request,'setup/staff.html', context)
                                            
            designation = request.POST.get('designation')
            if not designation:
                messages.error(request,'In valid designation')
                return render(request,'setup/staff.html', context)
                            
            branch = request.POST.get('branch')
            if not branch:
                messages.error(request,'Invalid brnach')
                return render(request,'setup/staff.html', context)
            branchid = Branch.objects.get(id=branch)


            email = request.POST.get('email')
            if not email:
                messages.error(request,'In valid email')
                return render(request,'setup/staff.html', context)
                            
            phonenumber = request.POST.get('phone')
            if not phonenumber:
                messages.error(request,'Invalid phone number')
                return render(request,'setup/staff.html', context)
            if  len(str(phonenumber)) <11 | len(str(phonenumber)):
                messages.error(request,'phone number must be 11 digits')
                return render(request,'setup/staff.html', context)

            Staff.objects.create(title=title,
                                 firstname=firstname,
                                 surname=surname,
                                 sex=sex,
                                 dateofbirth=dateofbirth,
                                 employmentdate=employmentdate,
                                 designation=designation,
                                 branch=branchid,
                                 email=email,
                                 phonenumber=phonenumber)

            messages.success(request, 'Staff Added successfully')
            return render(request,'setup/staff.html', context)

        return render(request, "setup/staff.html",{'error': 'Invalid request method'}, status=400)                    









