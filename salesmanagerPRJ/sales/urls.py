from django.urls import path
from . import views

urlpatterns = [
    path('get-staff/<int:branch_id>/', views.get_staff, name='get_staff'),
    path('get-facilities/<int:branch_id>/', views.get_facilities, name='get_facilities'),
    path('get-pumps/<int:facility_id>/', views.get_pumps, name='get_pumps'),
    path('get-products/<int:facility_id>/', views.get_products, name='get_products'),
    path('', views.index, name='sales_index'),
    path('record-sales/', views.record_sales, name='record_sales'),
    path('shift', views.create_shift, name="shift"),
    path('shift-management', views.shift_management, name ="shift_management"),
    path('shift-edit', views.edit_shift, name ="edit_shift")
]