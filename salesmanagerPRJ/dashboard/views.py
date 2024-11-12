from django.shortcuts import get_object_or_404, render, redirect
from setup.models import Staff, Branch, Storage, Price, Pump
from sales.models import Sales, Shift
from inventory.models import Inventory
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard(request):
    return render(request,'dashboard/main.html')

@login_required
def accountant_view(request, staff_id):
    branch_id = Staff.objects.values_list('branch_id', flat=True).get(id=staff_id)
    branches = Branch.objects.get(id=branch_id)
    shifts = Shift.objects.filter(branch_id=branch_id)
    sales = Sales.objects.filter(shift=shifts)

    sales = Sales.objects.filter(shift__branch=branches).select_related('shift', 'shift__branch')

    context = {
        'sales':sales,
        'shifts':shifts,
        'branches':branches
    }

    return render(request, 'dashboard/accountant.html', context)

@login_required
def attendant_view(request):

    staff_id = request.user.staff.id
    staff = Staff.objects.get(id=staff_id)
    shifts = Shift.objects.filter(staff_id=staff_id)
    sales = Sales.objects.filter(shift__staff=staff).select_related('shift', 'shift__staff')
    
    context = {
        'shifts':shifts,
        'sales':sales,
    }
    
    return context

@login_required
def manager_view(request):    
    
    staff_id = request.user.staff.id
    branch_id = Staff.objects.values_list('branch_id', flat=True).get(id=staff_id)

    shifts =Shift.objects.filter(branch_id=branch_id)
    inventories = Inventory.objects.filter(branch_id=branch_id)
    staff = Staff.objects.filter(branch_id=branch_id)
    branches = Branch.objects.get(id=branch_id)
    storages = Storage.objects.filter(branch_id=branch_id)
    prices = Price.objects.all()
    
    try:
        sales = Sales.objects.get(shift__branch=branches).select_related('shift', 'shift__branch')
    except Sales.DoesNotExist:
        sales = None

    context = {
        'shifts':shifts,
        'sales':sales,
        'inventories':inventories,
        'staff':staff,
        'branches':branches,
        'storages':storages,
        'prices':prices,
    }
    
    return context

@login_required
def md_view(request):
    
    shifts = Shift.objects.all()
    sales = Sales.objects.all()
    inventories = Inventory.objects.all()
    staff = Staff.objects.all()
    branches = Branch.objects.all()
    storages = Storage.objects.all()
    prices = Price.objects.all()

    context = {
        'shifts':shifts,
        'sales':sales,
        'inventories':inventories,
        'staff':staff,
        'branches':branches,
        'storages':storages,
        'prices':prices,
    
    }
    return context

@login_required
def supervisor_view(request):
    
    branch = request.user.staff.branch_id
    
    shifts =Shift.objects.filter(branch_id=branch)
    sales = Sales.objects.filter(branch_id=branch)
    inventories = Inventory.objects.filter(branch_id=branch)
    staff = Staff.objects.filter(branch_id=branch)
    storages = Storage.objects.filter(branch_id=branch)

    context = {
        'shifts':shifts,
        'sales':sales,
        'inventories':inventories,
        'staff':staff,
        'storages':storages,
    }
    
    return context

@login_required
def branch_view(request):
    
    role = request.user.role

    match role:
        case 'supervisor':
            context = supervisor_view(request)
            return render(request, 'dashboard/branch.html', context)
        case 'manager':
            context = manager_view(request)
            return render(request, 'dashboard/branch.html', context)
        case 'cashier':
            context = accountant_view(request)
            return render(request, 'dashboard/branch.html', context)
        case 'md':
            context = md_view(request)
            return render(request, 'dashboard/branch.html', context)

        case _:
            context = attendant_view(request)
            return render(request,'dashboard/branch.html', context)

@login_required
def product_view(request):
    role = request.user.role

    match role:
        case 'supervisor':
            context = supervisor_view(request)
            return render(request, 'dashboard/product.html', context)
        case 'manager':
            context = manager_view(request)
            return render(request, 'dashboard/product.html', context)
        case 'cashier':
            context = accountant_view(request)
            return render(request, 'dashboard/product.html', context)
        case 'md':
            context = md_view(request)
            return render(request, 'dashboard/product.html', context)

        case _:
            context = attendant_view(request)
            return render(request,'dashboard/product.html', context)

@login_required
def shift_view(request):

    role = request.user.role

    match role:
        case 'supervisor':
            context = supervisor_view(request)
            return render(request, 'dashboard/shift.html', context)
        case 'manager':
            context = manager_view(request)
            return render(request, 'dashboard/shift.html', context)
        case 'cashier':
            context = accountant_view(request)
            return render(request, 'dashboard/shift.html', context)
        case 'md':
            context = md_view(request)
            return render(request, 'dashboard/shift.html', context)

        case _:
            context = attendant_view(request)
            return render(request,'dashboard/shift.html', context)

@login_required
def sale_view(request):
    role = request.user.role

    match role:
        case 'supervisor':
            context = supervisor_view(request)
            return render(request, 'dashboard/sale.html', context)
        case 'manager':
            context = manager_view(request)
            return render(request, 'dashboard/sale.html', context)
        case 'cashier':
            context = accountant_view(request)
            return render(request, 'dashboard/sale.html', context)
        case 'md':
            context = md_view(request)
            return render(request, 'dashboard/sale.html', context)

        case _:
            context = attendant_view(request)
            return render(request,'dashboard/sale.html', context)
    return render(request,'dashboard/attendant.html')

@login_required
def current_month(request, staff_id):
    return render(request,'dashboard/attendant.html')
@login_required
def last_quarter(request, staff_id):
    return render(request,'dashboard/attendant.html')
@login_required
def year_on(request, staff_id):
    return render(request,'dashboard/attendant.html')
@login_required
def reconcile_sales(request,sale_id):
    return render(request,'dashboard/attendant.html')
