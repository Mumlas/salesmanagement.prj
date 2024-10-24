from datetime import date
from django.db import models
from setup.models import Staff, Pump, Branch, Product

# Create your models here.
class Shift(models.Model):
    type = models.CharField(max_length=20, unique=True, null=False)
    start = models.DateTimeField(unique=False, null=False)
    end = models.DateTimeField(unique=False, null=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="shift_staff", default=1)
    pump = models.ForeignKey(Pump, on_delete=models.CASCADE, related_name="shift_pump", default=1)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    quantity_sold = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_sales = models.DecimalField(max_digits=14, decimal_places=2, default=0.0)
    actual_sales = models.DecimalField(max_digits=14, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=False, null=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="shift_branch")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="shift_product")

    class Meta:
        verbose_name_plural="Shift"

    def __str__(self):
        return("Shift starts "+str(self.start)+" ends " +str(self.end))