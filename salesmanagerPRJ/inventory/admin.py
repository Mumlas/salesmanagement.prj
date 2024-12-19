from django.contrib import admin
from .models import Inventory, InventorySnapShot
# Register your models here.

@admin.register(Inventory)
class inventoryAdmin(admin.ModelAdmin):
    list_display = ('id','product','quantity','dateUpdated','updatedBy')
    list_filter = ('branch','product')

@admin.register(InventorySnapShot)
class InventorySnapShotAdmin(admin.ModelAdmin):
    list_display = ('id','inventory','inventory_id','product','quantity','date','updatedBy')
    list_filter = ('inventory','product')