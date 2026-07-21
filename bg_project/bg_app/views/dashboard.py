from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Brand, Product, Order

@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')
    
    section = request.GET.get('section', 'customer-management')
    
    context = {
        'section': section,
    }
    
    if section == 'customer-management':
        context['customers'] = User.objects.filter(is_staff=False)
        
    if section == 'brand-management':
        context['brands'] = Brand.objects.all().order_by('name')
        
    if section == 'product-management':
        context['products'] = Product.objects.all().order_by('-created_at')
        
    if section == 'order-fulfillment':
        context['orders'] = None
        
    if section == 'product-reviews':
        context['product_reviews'] = None
        
    if section == 'revenue-logs':
        context['revenue_logs'] = None
        
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def customer_dashboard_view(request):
    if request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')
    
    section = request.GET.get('section', 'pending-orders')
    
    context = {
        'section': section,
    }
    
    if section == 'pending-orders':
        context['pending_orders'] = Order.objects.exclude(customer=request.user, status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED]).order_by('-created_at')
    if section == 'my-orders':
        context['orders'] = None
    if section == 'my-reviews':
        context['my_reviews'] = None
    if section == 'total-spent':
        context['total_spent'] = None
    
    return render(request, 'dashboard/customer_dashboard.html', context)