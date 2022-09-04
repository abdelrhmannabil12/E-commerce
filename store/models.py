from ast import arg
from email.mime import image
from itertools import product
from traceback import print_exc
from django.db import models

from category.models import Category
from django.urls import reverse
# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=500,blank=True)
    price=models.IntegerField()
    images=models.ImageField(upload_to='images/products')
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    @property
    def get_url(self):
        return reverse("product_detail",args=[self.category.slug,self.slug])
    def __str__(self):
        return self.product_name