from django.contrib import admin
from .models import Product, Storage, Pump, Branch, Staff, Price

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','productName','productDescription',)

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('id','product','price',)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id','branchName', 'branchAddress',)
    
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'firstname','sex','dateofbirth','employmentdate',
                   'designation','branch','email','phonenumber')
    list_filter = ('branch','designation',)

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id','storageDesc','branch','product','capacity',)
    list_filter = ('branch',)

@admin.register(Pump)
class pumpAdmin(admin.ModelAdmin):
    list_display = ('id','pumpDesc','storage',)
    list_filter = ('storage',)
