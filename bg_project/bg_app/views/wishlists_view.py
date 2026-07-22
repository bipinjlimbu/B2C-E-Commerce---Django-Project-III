from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Wishlist

@login_required
def wishlist_view(request):
    return render(request, 'main/wishlist_page.html')