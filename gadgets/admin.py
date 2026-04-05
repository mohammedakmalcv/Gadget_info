from django.contrib import admin
from .models import Category, Brand, Product, Wishlist, Profile

# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Wishlist)   
admin.site.register(Profile)