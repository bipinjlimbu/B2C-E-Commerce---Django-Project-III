from django.urls import path
from .views.main_view import home_page
from .views.auth_view import register_view, login_view, logout_view
from .views.profile_view import profile_view, edit_profile_view, delete_profile_view
from .views.brands_view import add_brand_view, edit_brand_view, delete_brand_view
from .views.products_view import products_view, add_product_view, is_active_toggle_view, edit_product_view, delete_product_view, single_product_view
from .views.dashboard import admin_dashboard_view

urlpatterns = [
    path('', home_page, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/delete/<int:user_id>/', delete_profile_view, name='delete_profile'),
    path('brands/add/', add_brand_view, name='add_brand'),  
    path('brands/edit/<int:brand_id>/', edit_brand_view, name='edit_brand'),
    path('brands/delete/<int:brand_id>/', delete_brand_view, name='delete_brand'),
    path('products/', products_view, name='products'),
    path('products/add/', add_product_view, name='add_product'),
    path('products/toggle-status/<int:product_id>/', is_active_toggle_view, name='toggle_product_active'),
    path('products/edit/<int:product_id>/', edit_product_view, name='edit_product'),
    path('products/delete/<int:product_id>/', delete_product_view, name='delete_product'),
    path('products/<int:product_id>/', single_product_view, name='single_product'),
    path('dashboard/admin/', admin_dashboard_view, name='admin_dashboard'),
]