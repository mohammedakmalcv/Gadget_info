from django.db import models
from django.contrib.auth.models import User
#from .models import Product


class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # Links Brand to Category

    def __str__(self):
        return f"{self.name} ({self.category.name})"
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE) # Links Product to Brand
    price = models.DecimalField(max_digits=10, decimal_places=2)
    specs = models.TextField(help_text="Put all the cool specs here (RAM, Storage, etc.)")
    image_url = models.URLField(max_length=500, default="https://via.placeholder.com/300")
    gadget_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') # Prevents adding the same item twice

    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.product.name}"