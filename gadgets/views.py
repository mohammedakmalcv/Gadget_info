from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Wishlist, Profile 
from .forms import CustomUserCreationForm

from django.contrib import messages

def home(request, category_id=None):
    all_categories = Category.objects.all()
    wishlist_product_ids = []
    
    if request.user.is_authenticated:
        wishlist_product_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

    if category_id:
        gadgets_to_show = Product.objects.filter(brand__category__id=category_id)
        return render(request, 'home.html', {
            'gadgets': gadgets_to_show,
            'categories': all_categories,
            'active_category': category_id,
            'wishlist_product_ids': wishlist_product_ids  
        })
    else:
        category_products = {}
        for category in all_categories:
            products = Product.objects.filter(brand__category=category)[:4]
            if products.exists():
                category_products[category] = products
                
        return render(request, 'home.html', {
            'category_products': category_products,
            'categories': all_categories,
            'active_category': None,
            'wishlist_product_ids': wishlist_product_ids  
        })

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            form.save() 
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

#@login_required(login_url='login')
def product_detail(request, pk):
    
    gadget = Product.objects.get(id=pk)
    return render(request, 'detail.html', {'gadget': gadget})

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        
        wishlist_item.delete()
        messages.success(request, f"{product.name} was removed from your wishlist.")
    else:
        messages.success(request, f"{product.name} was added to your wishlist.")
        
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def profile_view(request):
    
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    
    recent_wishlist = Wishlist.objects.filter(user=request.user).order_by('-added_date')[:3]
    
    return render(request, 'profile.html', {
        'profile': profile,
        'recent_wishlist': recent_wishlist
    })