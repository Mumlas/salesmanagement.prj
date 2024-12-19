from django.db import models
from setup.models import Branch, Product, Storage,Staff


# Create your models here.
class Inventory(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="inventory_product")
    storage = models.ForeignKey(Storage, on_delete=models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    updatedBy = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    dateUpdated = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Inventory"

    def __str__(self) -> str:
        return(f'{self.quantity} liters of {self.product}, at {self.branch}')
    
class InventorySnapShot(models.Model):
    inventory=models.ForeignKey(Inventory, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=10, decimal_places=2,null=False, default=0.0)
    updatedBy = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Inventory History"

    def __str__(self) -> str:
        return(f'{self.quantity}  liters of  {self.product},  as of  {self.date}')
