from django.contrib import admin
from .models import Shift, Sales
# Register your models here.
@admin.register(Shift)
class shiftAdmin(admin.ModelAdmin):
    list_display = ('id','type','start','end','staff','branch','product','stock','is_active',)
    list_filter = ('is_active','branch','stock')


@admin.register(Sales)
class salesAdmin(admin.ModelAdmin):
    list_display = ('id','shift','quantity_sold','expected_sales','actual_sales','margin','reconciliation','remark')
    list_filter = ('quantity_sold','reconciliation')