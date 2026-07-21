from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Brand

@login_required
def add_brand_view(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')
    
    errors = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.FILES.get('logo')

        if not name:
            errors['name'] = 'Brand name is required.'
        elif Brand.objects.filter(name=name).exists():
            errors['name'] = 'Brand name already exists.'
            
        if not logo:
            errors['logo'] = 'Brand logo is required.'

        if errors:
            return render(request, 'main/add_brand_page.html', {'errors': errors, 'data': request.POST})

        brand = Brand(name=name, logo=logo)
        brand.save()
        
        messages.success(request, 'Brand added successfully.')
        return redirect('/dashboard/admin/?section=brand-management')
        
    return render(request, 'main/add_brand_page.html')

@login_required
def edit_brand_view(request, brand_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')
    
    brand = Brand.objects.get(id=brand_id)
    
    errors = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.FILES.get('logo')

        if not name:
            errors['name'] = 'Brand name is required.'
        elif Brand.objects.exclude(pk=brand_id).filter(name=name).exists():
            errors['name'] = 'Brand name already exists.'

        if errors:
            return render(request, 'main/edit_brand_page.html', {'errors': errors, 'data': request.POST, 'brand': brand})

        brand.name = name
        if logo:
            brand.logo = logo
        brand.save()
        
        messages.success(request, 'Brand updated successfully.')
        return redirect('/dashboard/admin/?section=brand-management')
    
    return render(request, 'main/edit_brand_page.html', {'brand': brand})