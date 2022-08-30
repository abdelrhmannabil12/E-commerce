from tabnanny import verbose
from django.db import models

# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(blank=True)
    category_img=models.ImageField(upload_to='images/category',blank=True)

    class Meta:
        verbose_name='Categorie'


    def __str__(self):
        return self.category_name