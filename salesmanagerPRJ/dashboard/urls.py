from . import views
from django.urls import path

urlpatterns = [
    path('accountant/', views.accountant_view, name='accountant'),
    path('dashboard-shift/', views.shift_view, name='dashboard-shift'),
    path('dashboard-sale/', views.sale_view, name='dashboard-sale'),
    path('manager/', views.manager_view, name='manager'),
    path('md_ceo/', views.md_view, name='md_ceo'),
    path('branch/', views.branch_view, name='branch'),
    path('product/', views.product_view, name='product'),
    path('sale/', views.product_view, name='sale'),
    path('', views.dashboard, name = 'main-dashboard')
]
