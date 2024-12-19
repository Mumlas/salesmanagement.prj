from django.db import models
from datetime import date
# Create your models here.

class Branch(models.Model):
    branchName = models.CharField(max_length=200, unique=True)
    branchAddress = models.CharField(max_length=200, null=False)

    class Meta:
        verbose_name_plural="Branches"

    def __str__(self):
        return(self.branchName)

class Product(models.Model):
    productName = models.CharField(max_length=100, unique=True)
    productDescription = models.CharField(max_length=200, null=True, default="None")

    class Meta:
        verbose_name_plural="Products"

    def __str__(self):
        return(self.productName)
        
class Storage(models.Model):
    storageDesc = models.CharField(max_length=100)
    capacity = models.DecimalField(max_digits=10, decimal_places=2)
    branch = models.ForeignKey(Branch,related_name='storage_branch', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="storage_product", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="Storage"

    def __str__(self):
        return(self.storageDesc+" "+ str(self.capacity)+" "+ str(self.branch))
    
class Price(models.Model):
    product = models.ForeignKey(Product, related_name="price_product", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        verbose_name_plural="Price"

    def __str__(self):
        return(self.product.productName+" "+ str(self.price))
    
class Pump(models.Model):
    pumpDesc = models.CharField(max_length=100, default="None")
    storage = models.ForeignKey(Storage, related_name='pump_storage', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="Pump"

    def __str__(self):
        return(self.pumpDesc)
    
# Staff
class Staff(models.Model):
    title = models.CharField(max_length=20)
    firstname = models.CharField(max_length=50, db_index=True)
    surname = models.CharField(max_length=50, db_index=True)
    dateofbirth = models.DateField()
    sex = models.CharField(max_length=10, null=False, db_index=True,default=1)
    employmentdate = models.DateField()
    designation = models.CharField(max_length=30, db_index=True)
    branch = models.ForeignKey(Branch, related_name='staff_branch', on_delete=models.CASCADE)
    email = models.EmailField(unique=True, null=True)
    phonenumber = models.BigIntegerField(unique=True, null=False)

    class Meta:
        verbose_name_plural="Staff"

    def __str__(self):
        return(self.firstname +" "+ self.surname)
    