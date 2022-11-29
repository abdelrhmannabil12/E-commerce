from itertools import product
from statistics import mode
from django.db import models
from store.models import *
# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=200)
    date_added=models.DateField(auto_now_add=True)


    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    variations=models.ManyToManyField(Variation,blank=True)
    is_active=models.BooleanField(default=True)

    @property
    def total(self):
        return self.product.price * self.quantity
    def __str__(self):
        return self.product.product_name