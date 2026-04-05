from django.db import models
from django.contrib.auth.models import User
#from .models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.category.name})"
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE) 
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
        unique_together = ('user', 'product') 

    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.product.name}"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, help_text="A little bit about your tech preferences.")
   
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()