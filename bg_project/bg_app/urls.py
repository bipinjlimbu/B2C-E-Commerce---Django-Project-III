from django.urls import path
from .views.main_view import home_page
from .views.auth_view import register_view, login_view, logout_view
from .views.profile_view import profile_view, edit_profile_view, delete_profile_view
from .views.brands_view import add_brand_view, edit_brand_view, delete_brand_view
from .views.products_view import products_view, add_product_view, is_active_toggle_view, edit_product_view, delete_product_view, single_product_view
from .views.cart_view import add_to_cart_view, cart_view, increase_quantity_view, decrease_quantity_view, remove_from_cart_view
from .views.payment_view import initiate_payment_view, payment_success_view, payment_failed_view
from .views.order_view import dispatch_order_view, deliver_order_view, order_completed_view, order_cancelled_view
from .views.reviews_view import add_review_view, edit_review_view, delete_review_view
from .views.dashboard import admin_dashboard_view, customer_dashboard_view

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
    path('cart/add/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('cart/increase/<int:product_id>/', increase_quantity_view, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', decrease_quantity_view, name='decrease_quantity'),
    path('cart/remove/<int:product_id>/', remove_from_cart_view, name='remove_from_cart'),
    path('payment/initiate/', initiate_payment_view, name='initiate_payment'),
    path('payment/success/', payment_success_view, name='payment_success'),
    path('payment/failed/', payment_failed_view, name='payment_failed'),
    path('order/dispatch/<int:order_id>/', dispatch_order_view, name='dispatch_order'),
    path('order/deliver/<int:order_id>/', deliver_order_view, name='deliver_order'),
    path('order/completed/<int:order_id>/', order_completed_view, name='order_completed'),
    path('order/cancelled/<int:order_id>/', order_cancelled_view, name='order_cancelled'),
    path('review/add/<int:product_id>/', add_review_view, name='add_review'),
    path('review/edit/<int:review_id>/', edit_review_view, name='edit_review'),
    path('review/delete/<int:review_id>/', delete_review_view, name='delete_review'),
    path('dashboard/admin/', admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/', customer_dashboard_view, name='customer_dashboard'),
]