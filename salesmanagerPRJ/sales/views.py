from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from setup.models import *
from inventory.models import Inventory
from django.contrib import messages
from datetime import datetime
from .models import Shift, Sales
from .forms import EditShiftForm, PostSalesForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request,'sales/index.html')

def record_sales(request):
    return render(request, 'sales/record_sales.html')

def get_staff(request, branch_id):
    attendants = Staff.objects.filter(branch_id=branch_id)
    print(f'Branch: {branch_id}, Staff: {attendants}')
    data = [{"id": a.id, "name": a.firstname +' '+a.surname} for a in attendants]
    return JsonResponse(data, safe=False)

def get_facilities(request, branch_id):
    facilities = Storage.objects.filter(branch_id=branch_id)
    data = [{"id": f.id, "name": f.storageDesc} for f in facilities]
    print(f'Branch: {branch_id}, Facilities: {data}')
    return JsonResponse(data, safe=False)

def get_pumps(request, facility_id):
    pumps = Pump.objects.filter(storage_id=facility_id)
    data = [{"id": p.id, "name": p.pumpDesc} for p in pumps]
    print(f'Facility: {facility_id}, Pumps: {data}')
    return JsonResponse(data, safe=False)

def get_products(request, facility_id, branch_id):
    print(f'Tank {facility_id} at Branch {branch_id}.')
    # SELECT productid FROM Storage WHERE faci
    product_id = Storage.objects.values_list('product_id', flat=True).get(id= facility_id, branch_id=branch_id)
    product = Product.objects.values_list('productName', flat=True).get(pk=product_id)
    print(f'product in the fcility {product}')

    try:
        inStock = Inventory.objects.values_list('quantity', flat=True).get(storage_id=facility_id, branch_id=branch_id, 
                                                                           product_id=product_id)
        print(f'Stock from get-products {inStock}')
        if not inStock:
            inStock=0
    except:
        print(f'Stock at facility {facility_id} for {product} is {inStock}')
        data = {
            "quantity":0
        }
    try:
        facility = Storage.objects.get(id=facility_id, branch_id=branch_id)
        print(f'Facility from get-products {facility}')
        if facility.product:
            product_name = facility.product.productName
        else:
            product_name="None"
    except:
        messages.error(request, 'In valid selection, check your inputs')
        return render(request,"sales/shift.html")
    data = {"product_name":product_name, 
            "inStock": inStock,
            "capacity":facility.capacity}
    return JsonResponse(data)

@login_required
def create_shift(request):
    # get branches
    branches =  Branch.objects.all()

    context = {
        'branches':branches,
    }

    user = request.user      

    if user.is_authenticated:
        print(user.role)
        if request.method=="GET":
            return render(request, "sales/shift.html", context)


        if request.method =="POST":

            type = request.POST.get('type')
            if not type:
                messages.error(request, 'Invalid type, select  valid type of shift')
                return render(request, 'sales/shift.html', context)

            start = request.POST.get('start')
            print(f'Start shift {start}')
            if not start:
                messages.error(request, 'date/time can not be empty, select date/time -Start Shift')
                return render(request, 'sales/shift.html', context)
            
            try:
                startShift = datetime.fromisoformat(start)
            except ValueError:
                messages.error(request, 'Invalid date/time, select  valid date/time - Start Shift')
                return render(request, 'sales/shift.html', context)                
            print(f'start shift {startShift} converted')

            stopShift = request.POST.get('stop')
            print(f'end shift {stopShift}')
            if not stopShift:
                messages.error(request, 'date/time can not be empty, select date/time - End shift')
                return render(request, 'sales/shift.html', context) 

            try:
                endShift = datetime.fromisoformat(stopShift)
            except ValueError:
                messages.error(request, 'Invalid date/time, select  valid date/time - End shift')
                return render(request, 'sales/shift.html', context)         

            pumpid = int(request.POST.get('pump'))
            pump = Pump.objects.get(id=pumpid)
            if not pump:
                messages.error(request, 'Invalid selection, select a valid pump')
                return render(request, 'sales/shift.html', context)
            
            product = request.POST.get('product')
            productid = Product.objects.values_list('id', flat=True).get(productName=product)
            product = Product.objects.get(id=productid)
            if not productid:
                messages.error(request, 'Invalid selection, select a valid pump')
                return render(request, 'sales/shift.html', context)
                    
            inStock = float(request.POST.get('stock'))
            isActive = request.POST.get('active')

            if inStock<0:
                messages.error(request, 'Stock is empty or invalid value entered')
                return render(request, 'sales/shift.html', context)
                                    
            branchid = int(request.POST.get('branch'))
            branch = Branch.objects.get(id=branchid)
            if not branch:
                messages.error(request, 'Invalid selection, select a valid branch')
                return render(request, 'sales/shift.html', context)                     

            isActive=False

            pump_attendant = int(request.POST.get('staff'))
            staff = Staff.objects.get(id=pump_attendant)
                
            Shift.objects.create(type=type,
                                    start = startShift,
                                    end=endShift,
                                    product=product,
                                    pump=pump,
                                    stock = inStock,
                                    staff = staff,
                                    branch = branch,
                                    is_active=isActive
                                    )
            messages.success(request, 'Shift Created successfully')
            return render(request,"sales/shift.html", context)

        return render(request, "sales/shift.html",{'error': 'Invalid request method'}, status=400)

def start_shift(request, shift_id):
    
    shift= Shift.object.filter(id=shift_id)
    shift.is_active=True
    shift.save()
    redirect('attendant-shift')


@login_required
def post_sales(request, pk):
    shift = get_object_or_404(Shift, pk=pk)
    form = PostSalesForm(isinstance=shift)

    context = {
        "form":form,
        "shift":shift,
    }

    form.fields['branch'].disabled=True
    form.fields['pump'].disabled=True
    form.fields['product'].disabled=True
    form.fields['stock'].disabled=True
    form.fields['type'].disabled=True
    form.fields['start'].disabled=True
    form.fields['end'].disabled=True
    form.fields['expected_sales'].disabled=True
    form.fields['is_active'].disabled=True

    if request.method == "POST":

        product = request.POST.get('product')
        productid = Product.objects.values_list('id', flat=True).get(productName=product)
        product = Product.objects.get(id=productid)

        if not productid:
            messages.error(request, 'Invalid selection, select a valid pump')
            return render(request, 'sales/shift.html', context)
        
        price = float(Price.objects.values_list('price', flat=True).get(product_id=productid))
        if not price:
            messages.error(request, 'No price template for the product, contact your supervisor')
            return render(request, 'sales/shift.html', context)

        inStock = float(request.POST.get('stock'))
        if inStock<0:
            messages.error(request, 'Stock is empty or invalid value entered')
            return render(request, 'sales/shift.html', context)
                                
        branchid = int(request.POST.get('branch'))
        branch = Branch.objects.get(id=branchid)
        if not branch:
            messages.error(request, 'Invalid selection, select a valid branch')
            return render(request, 'sales/shift.html', context)                     
           
        quantitySold = request.POST.get('quantitySold')
        if quantitySold =="":
            quantitySold=0
        quantitySold = float(quantitySold)

        isActive = request.POST.get('active')
        if isActive==True:
            if quantitySold <0:
                messages.error(request, 'Quantyt Sold can not less than zero')
                return render(request, 'sales/shift.html', context)              
            else:
                quantitySold = 0

        if quantitySold > inStock:
            messages.error(request, 'The quantity sold is more than the Stock, Adjust the quantity to atmost: '+str(quantitySold)) 
            return render(request, "sales/shift.html", context)        
        else:
            expected_sales = (quantitySold * price)

        if request.POST.get('quantity_sold') == "" and request.POST.get('actual_sales')=="":
            messages.error(request, 'Quantity and Sales can not be empty, enter "QUANTITY" or "TOTAL SALES"') 
            return render(request, "sales/post_sales.html", {"id":shift.id})
        else:
            actual_sales = float(request.POST.get('quantity_sold'))*price    
        
        diff = (actual_sales - expected_sales)
        
        Sales.objects.create(
            shift = shift,
            quantity_sold = quantitySold,
            actual_sales = actual_sales,
            expected_sales =  expected_sales,  # to be replace with price
            margin = diff,
            reconciliation =False
        )
        Shift.is_active=None
        Shift.save()
        Inventory.quantity = inStock-quantitySold #Adjust inventory
        Inventory.save()

        return redirect('sales_history')
    return render(request, 'sales/shift_history.html',{"user":shift.staff})

@login_required
def sales_history(request,id):
    staff = get_object_or_404(Sales, pk=id)
    
    context = {
        "staff":staff
    }

    return render(request, 'sales/sales_history.html', context)

@login_required
def shift_history(request,staff_id):
    staff = Staff.objects.get(pk=staff_id)
    shifts = Shift.objects.filter(staff=staff)
 
    context = {
        "shifts":shifts
    }

    return render(request, 'sales/shift_history.html', context)

@login_required
def shift_management(request,staff_id):
    #staff = Staff.objects.get(phonenumber=username)
    staff = Staff.objects.get(id=staff_id)
    
    shifts = Shift.objects.filter(staff=staff)
    context = {
        "shifts":shifts
    }
    return render(request, "sales/shift_management.html", context)

@login_required
def shift_edit(request, pk):

    shift = get_object_or_404(Shift, pk=pk)
    form = EditShiftForm(instance=shift)

    context = {
        "form":form,
        "shift":shift
    }

    form.fields['branch'].disabled=True
    form.fields['pump'].disabled=True
    form.fields['product'].disabled=True
    form.fields['stock'].disabled=True
    if request.method == "POST":

        try:
            shift.is_active = True if request.POST.get('is_active')=='on' else False
            shift.type = request.POST.get('type')
            shift.start = request.POST.get('start')
            shift.end = request.POST.get('end')
            shift.staff = Staff.objects.get(id= int(request.POST.get('staff')))
            shift.save()
        except ModuleNotFoundError:
            messages("Shift not defined")
            return render(request, "sales/shift_edit.html", context) 
        return redirect("shift_management")    
     
    return render(request, "sales/shift_edit.html", context)    

@login_required
def shift_remove(request, pk):
    
    shift = get_object_or_404(Shift, pk=pk)
    shift.delete()
    
    #return redirect("shift_management")
    return render(request,"sales/shift_management.html")    
