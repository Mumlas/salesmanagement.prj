from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'sales/index.html')

def record_sales(request):
    return render(request, 'sales/record_sales.html')
