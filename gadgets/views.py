from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .models import Product, Wishlist
from django.contrib import messages

def home(request, category_id=None):
    # 1. Grab all categories so we can make buttons out of them
    all_categories = Category.objects.all()
    
    # 2. If the customer clicked a specific category button...
    if category_id:
        gadgets_to_show = Product.objects.filter(brand__category__id=category_id)
    else:
        # If they didn't click a category, just show everything
        gadgets_to_show = Product.objects.all()
        
    # --- UPDATED: Grab just a list of saved Product IDs ---
    wishlist_product_ids = []
    if request.user.is_authenticated:
        # values_list('product_id', flat=True) creates a simple list like [1, 4, 9]
        wishlist_product_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        
    # Send gadgets, categories, and the list of saved IDs to the webpage
    return render(request, 'home.html', {
        'gadgets': gadgets_to_show,
        'categories': all_categories,
        'active_category': category_id,
        'wishlist_product_ids': wishlist_product_ids  # Pass the IDs here!
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # This is the magic line that saves credentials to db.sqlite3!
            return redirect('login') # Send them to the login page after they sign up
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url='login') # If they aren't logged in, send them to the login page!
def product_detail(request, pk):
    # Grab the specific gadget they clicked on using its ID (pk means Primary Key)
    gadget = Product.objects.get(id=pk)
    return render(request, 'detail.html', {'gadget': gadget})

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        # If it already exists, clicking the button again removes it
        wishlist_item.delete()
        messages.success(request, f"{product.name} was removed from your wishlist.")
    else:
        messages.success(request, f"{product.name} was added to your wishlist.")
        
    # Redirect back to the previous page
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})