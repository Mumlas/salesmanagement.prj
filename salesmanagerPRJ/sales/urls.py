from django.urls import path
from . import views

urlpatterns = [
    path('shift/get-staff/<int:branch_id>/', views.get_staff, name='get_staff'),
    path('shift/get-facilities/<int:branch_id>/', views.get_facilities, name='get_facilities'),
    path('shift/get-pumps/<int:facility_id>/', views.get_pumps, name='get_pumps'),
    path('shift/get-products/<int:facility_id>/<int:branch_id>/', views.get_products, name='get_products'),
    path('', views.index, name='sales-index'),
    path('record-sales/', views.record_sales, name='record-sales'),
    path('shift/', views.create_shift, name="shift"),
    path('shift-management/<int:staff_id>', views.shift_management, name ="shift-management"),
    path('shift-edit/<int:pk>', views.shift_edit, name ="shift-edit"),
    path('shift-remove/<int:pk>', views.shift_remove, name ="shift-remove"),
    path('shift/post-sales/<int:pk>', views.post_sales, name='post-sales'),
    path('shift/sales-history/<int:pk>', views.sales_history, name = 'sales-history'),
    path('shift/shift-history/<int:staff_id>', views.shift_history, name = 'shift-history'),
    path('shift/start-shift/', views.start_shift, name='start-shift'),
]