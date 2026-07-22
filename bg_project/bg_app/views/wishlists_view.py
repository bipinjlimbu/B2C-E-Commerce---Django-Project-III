from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Wishlist

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(customer=request.user).order_by('-added_at')
    return render(request, 'main/wishlist_page.html', {'wishlist_items': wishlist_items})

@login_required
def wishlist_toggle_view(request, product_id):
    wishlist_item, created = Wishlist.objects.get_or_create(customer=request.user, product_id=product_id)
    
    if not created:
        wishlist_item.delete()
        messages.success(request, 'Product removed from wishlist.')
    else:
        messages.success(request, 'Product added to wishlist.')
    
    return redirect(f'/products/{product_id}/')