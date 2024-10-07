from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from setup.models import Product, Storage
# Create your views here.


class Inventory(View):
    def get(self, request):
        facilities = Storage.objects.all()
        context = {
            'facilities':facilities,
            'values':request.POST
        }
        return render(request,'setup/product.html', context)
    
    def post(self, request):

        facilities = Storage.objects.all()
        capacity = Storage.objects.filter(pk facility)

        if request.method=="POST":
            facilityID = request.POST.get('facilityid')
            quantitySupplied = float(request.POST.get('quantitySupplied'))

            storageFacility = Storage.Objects.get(id=facilityID)
            product = Product.objects.get(storage=storageFacility)

            quantityRequired = storageFacility.quantity - product.storage

            if quantitySupplied <= quantityRequired:
                product.storage += quantityRequired

            else:
                messages.error(request, 'Select Product type')
                return render(request, 'setup/product.html', {'facilities':facilities})
            
            quantitySupplied = request.POST.get('quantitySupplied')
            if not product:
                messages.error(request, 'Enter the Quantity supplied')
                return render(request, 'setup/product.html', {'facilities':facilities})
            if quantitySupplied+currentQuantity > capacity:
                messages.error(request, 'The quantity is more than the capacity of the tank, Adjust the quanity to: ', {'available':available}) 
            
            dateSupplied = request.POST.get('dateSupplied')
            if not dateSupplied:
                messages.error(request, 'Select Date the Product was supplied')
                return render(request, 'setup/product.html', {'facilities':facilities}) 
            
            Product.objects.create(product=product,
                                storage = facility,
                                quantitySupplied = quantitySupplied,
                                dateSupplied =dateSupplied
                                )
            messages.success(request, 'Inventory Update successfully')
            return render(request,'setup/product.html', {'facilities':facilities})      