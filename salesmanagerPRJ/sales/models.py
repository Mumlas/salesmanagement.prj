from datetime import date
from django.db import models
from setup.models import Staff, Pump, Branch, Product
from inventory.models import Inventory

class Status(models.TextChoices):
    ONGOING = 'On-Going'
    PENDING = 'Pending'
    ENDED = 'Ended'

class SalesReconciliation(models.TextChoices):
    ONGOING = 'Reconciled'
    PENDING = 'Pending'

# Create your models here.
class Shift(models.Model):
    type = models.CharField(max_length=20, unique=False, null=False)
    start = models.DateTimeField(unique=False, null=False)
    end = models.DateTimeField(unique=False, null=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="shift_staff", default=1)
    pump = models.ForeignKey(Pump, on_delete=models.CASCADE, related_name="shift_pump", default=1)
    #stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(verbose_name='Status',max_length=100, choices=zip(Status,Status))
    #branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="shift_branch", null=True)
    #product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="shift_product", null=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='shift_inventory', null=True)


    class Meta:
        verbose_name_plural="Shift"

    def __str__(self):
        return( self.type  +" Shift on "+str(self.start))
    
class Sales(models.Model):
    shift = models.ForeignKey(Shift, related_name="sales_shift", on_delete=models.CASCADE)
    quantity_sold = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    expected_sales = models.DecimalField(max_digits=14, decimal_places=2, default=0.0)
    actual_sales = models.DecimalField(max_digits=14, decimal_places=2, default=0.0)
    margin = models.DecimalField(max_digits=14, decimal_places=2)
    reconciliation = models.CharField(verbose_name='Reconciliation',max_length=100, choices=zip(SalesReconciliation,SalesReconciliation))

    remark = models.TextField(max_length=1000, null=True)
    

    class Sales:
        verbose_name_plural ="Sales"

    def __str__(self):
        return(f"{self.quantity_sold} sold at {self.actual_sales}.")