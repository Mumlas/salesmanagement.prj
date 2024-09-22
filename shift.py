
# shift model

from django.db import models
from django.contrib.auth.models import User  # Assuming User model is for attendants

class Shift(models.Model):
    SHIFT_CHOICES = (
        ('MORNING', 'Morning Shift'),
        ('AFTERNOON', 'Afternoon Shift'),
    )
    
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supervisor')
    attendants = models.ManyToManyField(User, related_name='attendants')  # Many attendants in a shift
    shift_type = models.CharField(max_length=10, choices=SHIFT_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.shift_type} ({self.start_time} - {self.end_time}) at {self.branch.name}'

# shift schedulling
from django.shortcuts import render
from .models import Shift
from .forms import ShiftForm

def schedule_shift(request):
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect or give success message
    else:
        form = ShiftForm()
    
    return render(request, 'schedule_shift.html', {'form': form})

# creating a shift
from django import forms
from .models import Shift

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['branch', 'supervisor', 'attendants', 'shift_type', 'start_time', 'end_time']
        widgets = {
            'attendants': forms.CheckboxSelectMultiple(),  # To allow multiple attendants to be selected
        }

# shift tracking
class Sale(models.Model):
    attendant = models.ForeignKey(User, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    fuel_type = models.CharField(max_length=50)
    quantity_sold = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_time = models.DateTimeField(auto_now_add=True)

class Inventory(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    fuel_type = models.CharField(max_length=50)
    opening_level = models.DecimalField(max_digits=10, decimal_places=2)
    closing_level = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

# reconciliation
def shift_reconciliation_report(shift_id):
    shift = Shift.objects.get(id=shift_id)
    sales = Sale.objects.filter(shift=shift)
    inventory = Inventory.objects.filter(shift=shift)

    total_sales_amount = sum(sale.total_price for sale in sales)
    total_quantity_sold = sum(sale.quantity_sold for sale in sales)
    
    opening_level = sum(item.opening_level for item in inventory)
    closing_level = sum(item.closing_level for item in inventory)
    
    expected_closing_level = opening_level - total_quantity_sold
    
    reconciliation_status = 'Balanced' if expected_closing_level == closing_level else 'Discrepancy'
    
    return {
        'shift': shift,
        'total_sales_amount': total_sales_amount,
        'total_quantity_sold': total_quantity_sold,
        'opening_level': opening_level,
        'closing_level': closing_level,
        'reconciliation_status': reconciliation_status
    }

# Reporting
def generate_shift_report(branch_id, start_date, end_date):
    shifts = Shift.objects.filter(branch_id=branch_id, start_time__gte=start_date, end_time__lte=end_date)
    shift_reports = []

    for shift in shifts:
        report = shift_reconciliation_report(shift.id)
        shift_reports.append(report)

    return shift_reports
