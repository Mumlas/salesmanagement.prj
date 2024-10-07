from . import views
from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('branch', BranchView.as_view(), name='branch'),  
    path('product', ProductView.as_view(), name='product'),  
    path('pump', PumpView.as_view(), name='pump'),  
    path('shift', ShiftView.as_view(), name='shift'),  
    path('storage', StorageView.as_view(), name='storage'),  
    path('staff', StaffView.as_view(), name='staff'),  
]

