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
@csrf_exempt  # You might want to handle CSRF tokens properly in production
def update_inventory(request):
    # select the branch
    # select the product/facility: once the product is selcted from the particular branch, current stock can be retrived via storage faclity
    # get the capacity of the facility and determine the gap
    # fill in the gap using the available supplies -  raise alarm if the supplies will exceed the gap!!!

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"POST Request: {data}")

            branch_id = data.get('branch')
            facility_id = data.get('facility')
            product_id = data.get('product_name')
            inStock = data.get('inStock')
            capacity = data.get('capacity')
            quantitySupplied =request.POST.get('quantitySupplied')
            dateUpdated =request.POST.get('dateSupplied')

            # Check if the new quantity + current quantity is within capacity
            if inStock + quantitySupplied > capacity:
                return JsonResponse({'error': 'New supply exceeds facility capacity'}, status=400)

            # Update the current quantity in the facility
            quantity =  inStock + quantitySupplied
            Inventory.objects.create(branch=branch_id,
                                     product=product_id,
                                     storage=facility_id,
                                     quanityt = quantity,
                                     updatedBy = 1,
                                     dateUpdated=dateUpdated)

            messages.success(request, 'Inventory Updated successfully')
            return JsonResponse({'Current Stock': quantity})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
       
    return JsonResponse({'error': 'Invalid request method'}, status=400)