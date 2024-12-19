from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def custom(request, staff_id):
    return render(request, 'report/custom.html')

@login_required
def yearly(request, staff_id):
    return render(request,'report/year_on.html')

@login_required
def quarter(request, staff_id):
    return render(request,'report/quarterly.html')

@login_required
def monthly(request, staff_id):
    return render(request,'report/attendant.html')

@login_required
def weekly(request, staff_id):
    return render(request,'report/weekly.html')

@login_required
def reconcile_sales(request,sale_id):
    return render(request,'report/reconciliation.html')

@login_required
def daily(request, staff_id):
    return render(request,'report/daily.html')
