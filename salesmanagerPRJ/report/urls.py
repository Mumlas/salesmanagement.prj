from django.urls import path
from . import views

urlpatterns = [
        path('daily/', views.daily, name='daily'),
        path('reconciliation/', views.daily, name='reconciliation'),
        path('weekly/', views.daily, name='weekly'),
        path('monthly/', views.daily, name='monthly'),
        path('quarterly/', views.daily, name='quarterly'),
        path('yearly/', views.daily, name='yearly'),
        path('custom/', views.daily, name='custom'),
]
