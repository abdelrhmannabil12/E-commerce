from itertools import product
from tracemalloc import get_object_traceback
from unicodedata import category
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from category.models import Category
from .models import Product
from category.models import *
from cart.models import *
from cart.views import _cart_id
from django.core.paginator import *
from django.db.models import Q
# Create your views here.

def home(request):
    products=Product.objects.all().filter(is_available=True)

    return render(request,'home.html',{'products':products})

def store(request,category_slug=None):

    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True).order_by("id")
        product_count=products.count()
    else:     
        products=Product.objects.all().filter(is_available=True).order_by("id")
        product_count=products.count()
    paginator=Paginator(products,3)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    return render(request,"store.html",{'products':paged_products,
                                        'count':product_count})


def product_detail(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    return render(request,'product_detail.html',{"single_product":single_product,"in_cart":in_cart})



def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by("created_date").filter(Q(description__icontains=keyword) |  Q(product_name__icontains=keyword))
    return render(request,'store.html',{'products':products})