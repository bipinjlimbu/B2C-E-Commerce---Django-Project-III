from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Brand, Product, Order, Review
from django.db import models

@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')
    
    section = request.GET.get('section', 'customer-management')
    
    context = {
        'section': section,
        'awaiting_dispatch_count': Order.objects.filter(status=Order.Status.CONFIRMED).count(),
        'awaiting_delivery_count': Order.objects.filter(status=Order.Status.SHIPPING).count(),
        'delivered_count': Order.objects.filter(status=Order.Status.DELIVERED).count(),
        'completed_count': Order.objects.filter(status=Order.Status.COMPLETED).count(),
        'cancelled_count': Order.objects.filter(status=Order.Status.CANCELLED).count(),
        'total_gross_revenue': Order.objects.filter(status=Order.Status.COMPLETED).aggregate(total_revenue=models.Sum('total_amount'))['total_revenue'] or 0,
    }
    
    if section == 'customer-management':
        context['customers'] = User.objects.filter(is_staff=False)
        
    if section == 'brand-management':
        context['brands'] = Brand.objects.all().order_by('name')
        
    if section == 'product-management':
        context['products'] = Product.objects.all().order_by('-created_at')
        
    if section == 'order-fulfillment':
        context['orders'] = Order.objects.all().order_by('-created_at')
        
    if section == 'product-reviews':
        context['product_reviews'] = Review.objects.all().order_by('-created_at')
        
    if section == 'revenue-logs':
        context['revenue_logs'] = Order.objects.filter(status=Order.Status.COMPLETED).order_by('-created_at')
        
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def customer_dashboard_view(request):
    if request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')
    
    section = request.GET.get('section', 'pending-orders')
    
    context = {
        'section': section,
        'gross_spent': Order.objects.filter(customer=request.user, status=Order.Status.COMPLETED).aggregate(total_spent=models.Sum('total_amount'))['total_spent'] or 0,
        'average_spent': Order.objects.filter(customer=request.user, status=Order.Status.COMPLETED).aggregate(average_spent=models.Avg('total_amount'))['average_spent'] or 0,
    }
    
    if section == 'pending-orders':
        context['pending_orders'] = Order.objects.exclude(customer=request.user, status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED]).order_by('-created_at')
    if section == 'my-orders':
        context['orders'] = Order.objects.filter(customer=request.user, status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED]).order_by('-created_at')
    if section == 'my-reviews':
        context['my_reviews'] = Review.objects.filter(customer=request.user).order_by('-created_at')
    if section == 'total-spent':
        context['total_spent'] = Order.objects.filter(customer=request.user, status=Order.Status.COMPLETED).order_by('-created_at')
    
    return render(request, 'dashboard/customer_dashboard.html', context)