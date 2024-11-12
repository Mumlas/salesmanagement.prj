from django.urls import path
from . import views

urlpatterns = [  
    path('get-facilities/<int:branch_id>/', views.get_facilities, name='get_facilities'),
    path('get-products/<int:facility_id>/<int:branch_id>/', views.get_products, name='get_products'),
    path('get-quantity/<int:product_id>/', views.get_quantity, name='get_quantity'),
    path('', views.get_branches, name = 'get_branches'),
    path('update/', views.update_inventory, name='update')
    #path('', views.getInventory, name='get_inventory')
]