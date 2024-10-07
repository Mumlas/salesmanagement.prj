from django.contrib import admin
from .models import Product, Storage, Pump, Branch, Staff, Shift

# Register your models here.
admin.site.register(Product)
admin.site.register(Storage)
admin.site.register(Pump)
admin.site.register(Branch)
admin.site.register(Staff)
admin.site.register(Shift)
