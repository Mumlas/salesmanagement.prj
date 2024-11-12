from django.contrib import admin
from .models import Inventory
# Register your models here.

@admin.register(Inventory)
class inventoryAdmin(admin.ModelAdmin):
    list_display = ('id','branch','product','storage','quantity','dateUpdated','updatedBy')
    list_filter = ('branch','product')