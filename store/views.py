from itertools import product
from django.shortcuts import render
from .models import Product
# Create your views here.

def home(request):
    products=Product.objects.all().filter(is_available=True)

    return render(request,'home.html',{'products':products})

def store(request):
    products=Product.objects.all().filter(is_available=True)
    product_count=products.count()
    return render(request,"store.html",{'products':products,
                                        'count':product_count})