from django.http import JsonResponse
from django.shortcuts import render
from setup.models import *
from inventory.models import Inventory
from django.contrib import messages
from datetime import datetime
from .models import Shift


# Create your views here.
def index(request):
    return render(request,'sales/index.html')

def record_sales(request):
    return render(request, 'sales/record_sales.html')

def get_staff(request, branch_id):
    attendants = Staff.objects.filter(branch_id=branch_id)
    data = [{"id": a.id, "name": a.firstname +' '+a.surname} for a in attendants]
    return JsonResponse(data, safe=False)

def get_facilities(request, branch_id):
    facilities = Storage.objects.filter(branch_id=branch_id)
    data = [{"id": f.id, "name": f.storageDesc} for f in facilities]
    return JsonResponse(data, safe=False)

def get_pumps(request, facility_id):
    pumps = Pump.objects.filter(storage_id=facility_id)
    data = [{"id": p.id, "name": p.pumpDesc} for p in pumps]
    return JsonResponse(data, safe=False)

def get_products(request, facility_id):
    # SELECT productid FROM Storage WHERE faci
    product_id = Storage.objects.values_list('product_id', flat=True).get(pk= facility_id)
    product = Product.objects.values_list('productName', flat=True).get(pk=product_id)
    inStock=0
    
    try:
        inStock = Inventory.objects.values_list('quantity', flat=True).get(product_id=product_id)
        print(f'Stock from get-products {inStock}')
        facility = Storage.objects.get(id=facility_id)
        if not inStock:
            inStock=0
    except:
        data = {
            "quantity":0
        }
    try:
        facility = Storage.objects.get(id=facility_id)
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


def create_shift(request):
    # get branches
    branches =  Branch.objects.all()

    context = {
        'branches':branches
    }
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
        print(f'end shift {endShift} converted')

        print(f"Pump id: {request.POST.get('pump')}")

        pumpid = int(request.POST.get('pump'))
        pump = Pump.objects.get(id=pumpid)
        if not pump:
            messages.error(request, 'Invalid selection, select a valid pump')
            return render(request, 'sales/shift.html', context)
        
        product = request.POST.get('product')
        productid = Product.objects.values_list('id', flat=True).get(productName=product)
        product = Product.objects.get(id=productid)
        print(f'Product Name: {product}')
        print(f'Product ID: {productid}')
        if not productid:
            messages.error(request, 'Invalid selection, select a valid pump')
            return render(request, 'sales/shift.html', context)
                
        inStock = int(request.POST.get('stock'))
        isActive = request.POST.get('active')
        print(isActive)
        
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
        if isActive==True:
            if quantitySold <0:
                messages.error(request, 'Quantyt Sold can not less than zero')
                return render(request, 'sales/shift.html', context)              
            else:
                quantitySold = 0
        else:
            isActive=False
        
        print(f'Product {productid}')
        price = float(Price.objects.values_list('price', flat=True).get(product_id=productid))
        print(f'Price {price}')
        if not price:
            messages.error(request, 'No price template for the product, contact your supervisor')
            return render(request, 'sales/shift.html', context)
                
        if quantitySold > inStock:
            messages.error(request, 'The quantity sold is more than the Stock, Adjust the quantity to atmost: '+str(quantitySold)) 
            return render(request, "sales/shift.html", context)        
        else:
            totalSales = quantitySold * price
        
        print(f'Branch ID: {branchid}') 
        print(f'product ID: {productid} - {product}')
        print(f'Start Time:  - {startShift}')
        print(f'end Time:  - {endShift}')
        print(f'Selected product - {product}')
        print(f'Selected facility ID: {pump}')
        print(f'Current stock in {pump} is {inStock}')
        print(f'Product: {product}')
        print(f'Unit Price: {price}')
        print(f'Quantity Sold: {quantitySold}')
        print(f'Total Sales: {totalSales}')
        print(f'Active shift: {isActive}')  

        Shift.objects.create(type=type,
                                 start = startShift,
                                 end=endShift,
                                 product=product,
                                 pump=pump,
                                 stock = inStock,
                                 quantity_sold = quantitySold,
                                 total_sales =totalSales,
                                 #staff = user,
                                 branch = branch,
                                 is_active=isActive
                                 )
        messages.success(request, 'Shift Created successfully')
        return render(request,"sales/shift.html", context)

    return render(request, "sales/shift.html",{'error': 'Invalid request method'}, status=400)

def post_sales(request):
    pass

def shift_management(request):
    shifts = Shift.objects.all()

    context = {
        "shifts":shifts
    }
    return render(request, "sales/shift_management.html", context)

def edit_shift(request):
    pass