import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from setup.models import Product, Storage, Staff, Branch
from .models import Inventory
from django.views.decorators.csrf import csrf_exempt
from validation.models import CustomUser

def get_branches(request):
    branches = Branch.objects.all()
    context = {
        "branches":branches
    }
    return render(request, "inventory/update.html", context)

def get_facilities(request, branch_id):
    facilities = Storage.objects.filter(branch_id=branch_id)
    data = [{"id": f.id, "name": f.storageDesc} for f in facilities]
    print(f'selected facility: {data}')
    print('-----------------------------')
    return JsonResponse(data, safe=False)

def get_products(request, facility_id, branch_id):
    print(f'Branch id {branch_id}, Facility {facility_id}')
    product_id = Storage.objects.values_list('product_id', flat=True).get(pk= facility_id, branch_id=branch_id)
    print(f'branch id {branch_id} facility id {facility_id} and product id {product_id}')
    product = Product.objects.values_list('productName', flat=True).get(pk=product_id)
    inStock=0
    
    try:
        inStock = Inventory.objects.values_list('quantity', flat=True).get(product_id=product_id, branch_id=branch_id)
        print(f'Stock from get-products {inStock}')
        facility = Storage.objects.get(id=facility_id)
        if not inStock:
            inStock=0
    except:
        data = {
            "quantity":0
        }
    try:
        facility = Storage.objects.get(id=facility_id, branch_id=branch_id)
        if facility.product:
            product_name = facility.product.productName
            product_id = Product.objects.get(productName=product_name).id
        else:
            product_name="None"
    except:
        messages.error(request, 'In valid selection, check your inputs')
        return render(request,"inventory/update.html")
    data = {"product_name":product_name,
            "product_id":product_id,
            "inStock": inStock,
            "capacity":facility.capacity}
    return JsonResponse(data)

def get_quantity(request, product_id, branch_id, storage_id):
    inventory = Inventory.objects.get(product_id=product_id, branch_id=branch_id,storage_id=storage_id )
    return JsonResponse({"quantity": inventory.quantity})

def getInventory(request):
    branches = Branch.objects.all()
    context = {"branches":branches}
    return render(request, "inventory/update.html", context)

# Update inventory
#-@csrf_exempt  # You might want to handle CSRF tokens properly in production
@login_required(login_url='/validation/login/')
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

        user = request.user

        if user is not None:
            staff = Staff.objects.get(id=user.staff.id)


            print(f'Branch ID : {branchid}') 
            print(f'product ID : {productid} - {product}')
            print(f'List of facilities in Branch {branchid}  - {facilities}')
            print(f'Selected product - {product}')
            print(f'Selected facility ID: {facilityid}')            
            print(f'Capacity of facility {facilityid} - {capacity}')
            print(f'Current stock in {facilityid} is {inStock}')  
            print(f'Updated by {staff}')          


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
                return redirect('get_branches')        

            dateSupplied = request.POST.get('dateSupplied')
            if not dateSupplied:
                messages.error(request, 'Select Date the Product was supplied')
                return redirect('get_branches')
            print(f'Data type of {branchid} is {type(branch)}')
            Inventory.objects.create(product=productid,
                                    storage = facility,
                                    quantity = inStock,
                                    dateUpdated =dateSupplied,
                                    updatedBy = staff,
                                    branch = branch
                                    )
            messages.success(request, 'Inventory Update successfully')
            return redirect('get_branches')

    return redirect('get_branches')