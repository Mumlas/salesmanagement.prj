from django.urls import path
from . import views

urlpatterns = [
    path('shift/get-staff/<int:branch_id>/', views.get_staff, name='get-taff'),
    path('shift/get-facilities/<int:inventory_id>/', views.get_facilities, name='get-facilities'),
    path('shift/get-pumps/<int:facility_id>/', views.get_pumps, name='get-pumps'),
    path('shift/get-products/<int:facility_id>/<int:branch_id>/', views.get_products, name='get-products'),
    path('', views.index, name='sales-index'),
    path('record-sales/', views.record_sales, name='record-sales'),
    path('shift/', views.create_shift, name="shift"),
    path('shift-management/<int:staff_id>', views.shift_management, name ="shift-management"),
    path('shift-edit/<int:pk>', views.shift_edit, name ="shift-edit"),
    path('new-shift/<int:pk>', views.new_shift, name ="new-shift"),
    path('shift-remove/<int:pk>', views.shift_remove, name ="shift-remove"),
    path('shift/post-sales/<int:pk>', views.post_sales, name='post-sales'),
    path('shift/sales-history/', views.sales_history, name = 'sales-history'),
    path('shift/shift-history/<int:staff_id>', views.shift_history, name = 'shift-history'),
    path('shift/start-shift/<int:shift_id>', views.start_shift, name='start-shift'),
    path('shift/reconcile_sale/<int:pk>', views.reconcile_sale, name='reconcile-sale'),
    path('shift/get-branch/<int:inventory_id>/', views.get_branch, name = 'get-branch'),
    path('shift/bulk-shifts/', views.bulk_shifts, name='bulk-shifts'),
    path('shift/post-sales/get-price/<str:productName>/', views.get_price, name='get-price'),
]