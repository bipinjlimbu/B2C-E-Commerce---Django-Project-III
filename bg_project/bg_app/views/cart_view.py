from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Brand, Product, Cart, CartItem

@login_required
def add_to_cart_view(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if CartItem.objects.filter(cart__customer=request.user, product=product).exists():
        messages.info(request, f"{product.name} is already in your cart.")
        return redirect('products')
    
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect('products')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.total_price for item in cart_items)
    
    return render(request, 'main/cart_page.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def increase_quantity_view(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if not CartItem.objects.filter(cart__customer=request.user, product=product).exists():
        messages.error(request, f"{product.name} is not in your cart.")
        return redirect('cart')
    
    if product.stock <= 0:
        messages.error(request, f"{product.name} is out of stock.")
        return redirect('cart')
    
    cart_item = CartItem.objects.get(cart__customer=request.user, product=product)
    
    if cart_item.quantity >= product.stock:
        messages.error(request, f"You cannot add more of {product.name} to your cart. Only {product.stock} left in stock.")
        return redirect('cart')
    
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')