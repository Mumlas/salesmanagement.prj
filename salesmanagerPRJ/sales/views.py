import json
from setup.models import *
from datetime import datetime
from django.db.models import Q
from .models import Shift, Sales
from django.contrib import messages
from django.http import JsonResponse
from inventory.models import Inventory
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import EditShiftForm, ReconcileSalesForm, NewShiftForm


# Create your views here.
def index(request):
    return render(request,'sales/index.html')

@login_required
def record_sales(request):
    return render(request, 'sales/record_sales.html')

@login_required
def get_branch(request, inventory_id):
    inventory = Inventory.objects.get(id=inventory_id)
    branches = Branch.objects.filter(id = inventory.branch_id)
    data = [{"id": b.id, "name":b.branchName} for b in branches]
    print(data)
    return JsonResponse(data, safe=False)

@login_required
def get_staff(request, branch_id):
    attendants = Staff.objects.filter(branch_id=branch_id, designation='pump_attendant')
    data = [{"id": a.id, "name": a.firstname +' '+a.surname} for a in attendants]
    print(data)
    return JsonResponse(data, safe=False)

@login_required
def get_facilities(request, inventory_id):
    inventory = Inventory.objects.get(id=inventory_id)
    facilities = Storage.objects.filter(id = inventory.storage_id)
    data = [{"id": f.id, "name": f.storageDesc} for f in facilities]
    return JsonResponse(data, safe=False)

@login_required
def get_pumps(request, facility_id):
    pumps = Pump.objects.filter(storage_id=facility_id)
    data = [{"id": p.id, "name": p.pumpDesc} for p in pumps]
    return JsonResponse(data, safe=False)

@login_required
def get_products(request, facility_id, branch_id):
    # SELECT productid FROM Storage WHERE faci
    product_id = Storage.objects.values_list('product_id', flat=True).get(id= facility_id, branch_id=branch_id)
    product = Product.objects.values_list('productName', flat=True).get(pk=product_id)

    try:
        inStock = Inventory.objects.values_list('quantity', flat=True).get(storage_id=facility_id, branch_id=branch_id, 
                                                                           product_id=product_id)
        if not inStock:
            inStock=0
    except:
        print(f'Stock at facility {facility_id} for {product} is {inStock}')
        data = {
            "quantity":0
        }
    try:
        facility = Storage.objects.get(id=facility_id, branch_id=branch_id)
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
def bulk_shifts(request):
   
   try:
        #the request body is accessed using request.body, which contains the raw request payload
    data = request.body
    # data is a bytes-like object, so you might want to convert it to a dictionary or a string
    data = data.decode('utf-8')
    # parse the JSON data
    data = json.loads(data)
    # now you can access the data as a dictionary
    #data= data['mapping']
    request.session['data']=data

    return JsonResponse(data, safe=False)
   except json.JSONDecodeError:
       return JsonResponse({'error': 'Bad request'}, status=400)

@login_required
def create_shift(request):
    # get branches
    branch_id = request.user.staff.branch_id
    branches =  Branch.objects.all()
    inventories = Inventory.objects.filter(branch_id=branch_id)

    context = {
        'branches':branches,
        'inventory':inventories,
        'branch_id':branch_id,
    }

    user = request.user      

    if user.is_authenticated:
        if request.method=="GET":
            return render(request, "sales/shift.html", context)


        if request.method =="POST":
            print(f'Bulk shift: {bulk_shifts(request)}')

            try:
                data= request.session['data']
                #body_unicode = request.body.decode('utf-8')
                #print(body_unicode)
                #data = json.loads(body_unicode)
                mapping = data['mapping']
                #mapping = bulk_shifts(request)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON data: {str(e)}'}, status=400)

            inventory_id = int(request.POST.get('inventory'))
            if not inventory_id:
                messages.error(request, 'Invalid value assign to inventory')
                return render(request, 'sales/shift.html', context)
            
            try:
                inventory = Inventory.objects.get(id=inventory_id)
            except Inventory.DoesNotExist:
                messages.error(request, 'Can not find the selected inventory')
                return render(request, 'sales/shift.html', context)
            
            type = request.POST.get('type')
            if not type:
                messages.error(request, 'Invalid type, select  valid type of shift')
                return render(request, 'sales/shift.html', context)

            start = request.POST.get('start')
            if not start:
                messages.error(request, 'date/time can not be empty, select date/time -Start Shift')
                return render(request, 'sales/shift.html', context)
            
            try:
                startShift = datetime.fromisoformat(start)
            except ValueError:
                messages.error(request, 'Invalid date/time, select  valid date/time - Start Shift')
                return render(request, 'sales/shift.html', context)                

            stopShift = request.POST.get('stop')
            if not stopShift:
                messages.error(request, 'date/time can not be empty, select date/time - End shift')
                return render(request, 'sales/shift.html', context) 

            try:
                endShift = datetime.fromisoformat(stopShift)
            except ValueError:
                messages.error(request, 'Invalid date/time, select  valid date/time - End shift')
                return render(request, 'sales/shift.html', context)         

            """pumpid = int(request.POST.get('pump'))
            pump = Pump.objects.get(id=pumpid)
            if not pump:
                messages.error(request, 'Invalid selection, select a valid pump')
                return render(request, 'sales/shift.html', context)"""
            
            product = request.POST.get('product')
            productid = Product.objects.values_list('id', flat=True).get(productName=product)
            product = Product.objects.get(id=productid)
            if not productid:
                messages.error(request, 'Invalid selection, select a valid pump')
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

            """pump_attendant = int(request.POST.get('staff'))
            staff = Staff.objects.get(id=pump_attendant)"""

            for i in range(len(mapping)):
                shift = Shift.objects.create(
                pump_id = mapping[i]["pump"],
                staff = Staff.objects.get(id=mapping[i]["agent"]),
                end=endShift,
                start=startShift,
                status='Pending',
                inventory=inventory,
                type=type
                )
                print(f'Shifts: {shift}')
                exist = existing_shift(shift)
                if not exist:
                    raise ValidationError(f'Shift overlaps with another shift for { shift.staff } on { shift.start }.')
                else:
                    shift.save()

                
                
            """Shift.objects.create(type=type,
                                    start = startShift,
                                    end=endShift,
                                    pump=pump,
                                    staff = staff,
                                    status='Pending',
                                    inventory=inventory,
                                    )"""
            messages.success(request, 'Shift Created successfully')
            return render(request,"sales/shift.html", context)

        return render(request, "sales/shift.html",{'error': 'Invalid request method'}, status=400)

@login_required
def start_shift(request, shift_id):
    
    shift= Shift.objects.get(id=shift_id)
    print(shift)
    shift.status='On-Going'
    shift.save()

    return redirect('dashboard-shift')

@login_required
def post_sales(request, pk):
    
    shift = get_object_or_404(Shift, pk=pk)

    inventory = get_object_or_404(Inventory, pk=shift.inventory_id)
    products = Price.objects.all().select_related()

    context = {
        "inventory":inventory,
        "shift":shift,
        "products":products
    }
    
    if request.method == "POST":

        staff_id = request.user.staff.id
        product = request.POST.get('product')
        productid = Product.objects.values_list('id', flat=True).get(productName=product)
        product = Product.objects.get(id=productid)

        if not product:
            messages.error(request, 'Invalid selection, select a valid pump')
            return render(request, 'sales/shift.html', context)
        
        price = float(Price.objects.values_list('price', flat=True).get(product_id=productid))
        if not price:
            messages.error(request, 'No price template for the product, contact your supervisor')
            return render(request, 'sales/shift.html', context)

        inStock = request.POST.get('openingStock')

        inStock = float(request.POST.get('openingStock'))
        if inStock<0:
            messages.error(request, 'Stock is empty or invalid value entered')
            return render(request, 'sales/shift.html', context)
                                
        branchid = request.POST.get('branch')
        branch = Branch.objects.get(branchName=branchid)
        if not branch:
            messages.error(request, 'Invalid selection, select a valid branch')
            return render(request, 'sales/shift.html', context)                     
           
        quantitySold = request.POST.get('quantitySold')
        if quantitySold =="":
            quantitySold=0
        else:
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
            expectedSales = (quantitySold * price)

        if request.POST.get('quantitySold') == "" and request.POST.get('actualSales')=="":
            messages.error(request, 'Quantity and Sales can not be empty, enter "QUANTITY" or "TOTAL SALES"') 
            return render(request, "sales/post_sales.html", {"id":shift.id})
        else:
            actualSales = float(request.POST.get('actualSales'))   
        
        diff = (actualSales - expectedSales)
        
        Sales.objects.create(
            shift = shift,
            quantity_sold = quantitySold,
            actual_sales = actualSales,
            expected_sales =  expectedSales,  # to be replace with price
            margin = diff,
            reconciliation =""
        )
        shift.status='Ended'
        shift.save()
        inventory.quantity = inStock-quantitySold #Adjust inventory
        inventory.save()
        print(f'Post-sales: {staff_id}')
        return redirect('dashboard-sale')
    return render(request, 'sales/post_sales.html', context)

@login_required
def sales_history(request):
    staff = Staff.objects.get(id=request.user.staff_id)
    shifts = Shift.objects.filter(staff=staff)
    sales = Sales.objects.filter(shift__staff=staff).select_related('shift', 'shift__staff')

    
    print(sales)
    context = {
        "staff":staff,
        "sales":sales,
        "shifts":shifts,
    }
    return redirect('sale-view')
    #return render(request, 'sales/sales_history.html', context)

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
            shift.status = True if request.POST.get('status')=='on' else False
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
def new_shift(request, pk):

    shift = get_object_or_404(Shift, pk=pk)
    form = NewShiftForm(instance=shift)

    context = {
        "form":form,
        "shift":shift
    }

    form.fields['staff'].disabled=True
     
    return render(request, "sales/new_shift.html", context)

@login_required
def shift_remove(request, pk):
    
    shift = get_object_or_404(Shift, pk=pk)
    shift.delete()
    
    #return redirect("shift_management")
    return render(request,"sales/shift_management.html")

@login_required
def reconcile_sale(request, pk):

    products = Price.objects.all().select_related()

    sale = get_object_or_404(Sales, pk=pk)
    form = ReconcileSalesForm(instance=sale)

    context = {
        "form":form,
        "sale":sale,
        "products":products,
    }

    if request.method == 'POST':
        reconciliation = request.POST.get('reconciliation')
        expected_sales = request.POST.get('expected_sales')
        actual_sales = request.POST.get('actual_sales')
        margin = request.POST.get('margin')
        remark = request.POST.get('remark')

        try:
            expected_sales = float(expected_sales)
            actual_sales = float(actual_sales)

            if expected_sales <= actual_sales:
                reconciliation = 'Reconciled'
            else:
                remark = remark + ', there is a difference of ' + str(margin)
                reconciliation = "Pending"

            sale.reconciliation = reconciliation
            sale.remark = remark
            sale.save()
            return redirect('dashboard-sale')

        except:
            messages.error(request, 'Invalid input parameter detected')
            return render(request,'sales/reconcile_sales.html', context)
        
    return render(request,'sales/reconcile_sales.html', context)

def get_price(request, productName):

    product = Product.objects.get(productName=productName)
    prices = Price.objects.get(product=product)
    
    data = {"id": prices.id, "name": prices.price}
    return JsonResponse(data, safe=False)

        
def existing_shift(shift):
    # Check for overlapping shifts
    overlapping_shifts = Shift.objects.filter(
        staff=shift.staff,start=shift.start)
    print(f'Overlap: {overlapping_shifts}')
    if overlapping_shifts is not None:
        return True
    else:
        return False
    
def save(self, *args, **kwargs):
    self.clean()
    super().save(*args, **kwargs)
#Model level validation

def validate_bulk_shifts(shifts):
    for i, shift in enumerate(shifts):
        # Check against shifts already in the database
        overlapping_shifts = Shift.objects.filter(
            Q(staff=shift.staff),
            Q(date=shift.date),
            Q(
                Q(start_time_lt=shift.end_time, start_time_gte=shift.start_time) |
                Q(end_time_gt=shift.start_time, end_time_lte=shift.end_time) |
                Q(start_time_lte=shift.start_time, end_time_gte=shift.end_time)
            )
        )
        if overlapping_shifts.exists():
            raise ValidationError(f"Shift overlaps with another shift for { shift.staff } on { shift.start }")
        
        """
        Q(
            Q(start_lt=shift.end, start_gte=shift.start) |
            Q(end_gt=shift.start, end__lte=shift.end) |
            Q(start_lte=shift.start, end_gte=shift.end)
        )
        """