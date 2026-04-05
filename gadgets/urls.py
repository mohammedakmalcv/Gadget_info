from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('category/<int:category_id>/', views.home, name='category_filter'),
    path('signup/', views.signup, name='signup'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('profile/', views.profile_view, name='profile'),
]