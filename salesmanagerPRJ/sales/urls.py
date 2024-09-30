from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='sales_index'),
    path('record-sales', views.record_sales, name='record_sales'),

]