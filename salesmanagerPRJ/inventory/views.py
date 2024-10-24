import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from setup.models import Product, Storage, Staff, Branch
from .models import Inventory
from django.views.decorators.csrf import csrf_exempt

def get_branches(request):
    branches = Branch.objects.all()
    context = {
        "branches":branches
    }
    return render(request, "inventory/update.html", context)

def get_facilities(request, branch_id):
    facilities = Storage.objects.filter(branch_id=branch_id)
    data = [{"id": f.id, "name": f.storageDesc} for f in facilities]
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
        return render(request,"inventory/update.html")
    data = {"product_name":product_name, 
            "inStock": inStock,
            "capacity":facility.capacity}
    return JsonResponse(data)

def get_quantity(request, product_id):
    inventory = Inventory.objects.get(product_id=product_id)
    print(f'Current quantity: {inventory}')
    return JsonResponse({"quantity": inventory.quantity})

def getInventory(request):
    branches = Branch.objects.all()
    context = {"branches":branches}
    return render(request, "inventory/update.html", context)

# Update inventory
#-@csrf_exempt  # You might want to handle CSRF tokens properly in production
def update_inventory(request):

    branches = Branch.objects.all()
    context = {"branches":branches}

    if request.method == "POST":
        #form_data = inventoryForm()

    # select the branch
    # select the product/facility: once the product is selcted from the particular branch, current stock can be retrived via storage faclity
    # get the capacity of the facility and determine the gap
    # fill in the gap using the available supplies -  raise alarm if the supplies will exceed the gap!!!

        branchid = int(request.POST.get('branch'))
        branch = Branch.objects.get(id=branchid)

        product = request.POST.get('product')
        facilityid = int(request.POST.get('facility'))
        facility = Storage.objects.get(id=facilityid)

        inStock = float(request.POST.get('quantityinStock'))

        productid = Product.objects.get(productName=product)
        facilities = Storage.objects.filter(branch_id=branchid)
        capacity = float(Storage.objects.values_list('capacity', flat=True).get(pk= facilityid))

        print(f'Branch ID : {branchid}') 
        print(f'product ID : {productid} - {product}')
        print(f'List of facilities in Branch {branchid}  - {facilities}')
        print(f'Selected product - {product}')
        print(f'Selected facility ID: {facilityid}')            
        print(f'Capacity of facility {facilityid} - {capacity}')
        print(f'Current stock in {facilityid} is {inStock}')            


        quantitySupplied = float(request.POST.get('quanitySupplied'))
        quantityRequired = capacity - inStock

        print(f'Product: {product}')
        print(f'Storage Facility: {facilityid}')
        print(f'Quantity Supplied: {quantitySupplied}')
        print(f'Quantity Required: {quantityRequired}')
        
        if quantitySupplied <= quantityRequired:
            inStock += quantitySupplied
            print(f'New Stock {inStock}')
        else:
            messages.error(request, 'The quantity is more than the capacity of the tank, Adjust the quanity to: '+str(quantityRequired)) 
            return render(request, "inventory/update.html", context)        

        dateSupplied = request.POST.get('dateSupplied')
        if not dateSupplied:
            messages.error(request, 'Select Date the Product was supplied')
            return render(request, 'inventory/update.html', context) 
        print(f'Data type of {branchid} is {type(branch)}')
        Inventory.objects.create(product=productid,
                                 storage = facility,
                                 quantity = inStock,
                                 dateUpdated =dateSupplied,
                                 updatedBy = user,
                                 branch = branch
                                 )
        messages.success(request, 'Inventory Update successfully')
        return render(request,'inventory/update.html', context)

    return render(request, "inventory/update.html",{'error': 'Invalid request method'}, status=400)