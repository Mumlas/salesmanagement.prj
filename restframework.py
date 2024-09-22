
'''
A REST API (Representational State Transfer) follows principles that define how 
applications communicate over HTTP. It uses HTTP methods like GET, POST, PUT, 
DELETE to perform CRUD operations.

SETTING UP a RESTful API in django
'''
# install djangorestfrakework
pip install djangorestframework

#Define Models: Use Django models to represent your database tables (e.g., Branch, User, Shift, Sale, etc.).
from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)

class Sale(models.Model):
    attendant_shift = models.ForeignKey('AttendantShift', on_delete=models.CASCADE)
    fuel_type = models.CharField(max_length=50)
    quantity_sold = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_time = models.DateTimeField(auto_now_add=True)


# Create Serializers: Serializers in DRF convert Django models to JSON data for the API.
from rest_framework import serializers
from .models import Branch, Sale

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'location', 'manager']

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'attendant_shift', 'fuel_type', 'quantity_sold', 'total_price', 'sale_time']


# Create Views: Views define how requests are handled. You can create API views to perform CRUD operations on the models.

from rest_framework import viewsets
from .models import Branch, Sale
from .serializers import BranchSerializer, SaleSerializer

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


# Define API Routes: Use Django’s urls.py to define API routes. This is where RESTful endpoints will be mapped.

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BranchViewSet, SaleViewSet

router = DefaultRouter()
router.register(r'branches', BranchViewSet)
router.register(r'sales', SaleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

''' API Usage:

GET /api/branches/: Fetch all branches.
POST /api/branches/: Create a new branch.
PUT /api/branches/{id}/: Update an existing branch.
DELETE /api/branches/{id}/: Delete a branch.
You can test these endpoints with tools like Postman or cURL.

Pros of REST:
Simple and easy to implement.
Built-in support for HTTP methods and status codes.
Well-suited for standard CRUD operations.
'''