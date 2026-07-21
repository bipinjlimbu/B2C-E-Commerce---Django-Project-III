from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
        context['customers'] = None
        
    if section == 'brand-management':
        context['brands'] = None
        
    if section == 'product-management':
        context['products'] = None
        
    if section == 'order-fulfillment':
        context['orders'] = None
        
    if section == 'product-reviews':
        context['product_reviews'] = None
        
    if section == 'revenue-logs':
        context['revenue_logs'] = None
        
    return render(request, 'dashboard/admin_dashboard.html', context)