from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Brand, Product

@login_required
def add_product_view(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')

    brands = Brand.objects.all().order_by('name')
    
    errors = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        condition = request.POST.get('condition')
        sku = request.POST.get('sku')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        brand_id = request.POST.get('brand')
        product_image = request.FILES.get('product_image')
        is_active = request.POST.get('is_active') == 'true'

        if not name:
            errors['name'] = 'Product name is required.'
        if not description:
            errors['description'] = 'Product description is required.'
        if not category:
            errors['category'] = 'Product category is required.'
        if not condition:
            errors['condition'] = 'Product condition is required.'
            
        if not sku:
            errors['sku'] = 'Product SKU is required.'
        elif Product.objects.filter(sku=sku).exists():
            errors['sku'] = 'Product SKU already exists.'    
        
        if not price:
            errors['price'] = 'Product price is required.'
        if not stock:
            errors['stock'] = 'Product stock is required.'
        if not brand_id:
            errors['brand'] = 'Product brand is required.'
        if not product_image:
            errors['product_image'] = 'Product image is required.'

        if errors:
            return render(request, 'main/add_product_page.html', {'brands':brands, 'errors': errors, 'data': request.POST})

        brand = Brand.objects.get(id=brand_id)
        product = Product(
            name=name,
            description=description,
            category=category,
            condition=condition,
            sku=sku,
            price=price,
            stock=stock,
            brand=brand,
            product_image=product_image,
            is_active=is_active
        )
        product.save()

        messages.success(request, 'Product added successfully.')
        return redirect('/dashboard/admin/?section=product-management')
    
    return render(request, 'main/add_product_page.html', {'brands': brands})

@login_required
def is_active_toggle_view(request, product_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')
    
    product = Product.objects.get(id=product_id)
    
    if not product:
        messages.error(request, "Product not found.")
        return redirect('/dashboard/admin/?section=product-management')
    
    product.is_active = not product.is_active
    product.save()
    
    status = 'activated' if product.is_active else 'deactivated'
    
    messages.success(request, f'Product {status} successfully.')
    return redirect('/dashboard/admin/?section=product-management')

@login_required
def edit_product_view(request, product_id):
    product = Product.objects.get(id=product_id)
    brands = Brand.objects.all().order_by('name')
    
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')
    
    if not product:
        messages.error(request, "Product not found.")
        return redirect('/dashboard/admin/?section=product-management')
    
    errors = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        condition = request.POST.get('condition')
        sku = request.POST.get('sku')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        brand_id = request.POST.get('brand')
        product_image = request.FILES.get('product_image')

        if not name:
            errors['name'] = 'Product name is required.'
        if not description:
            errors['description'] = 'Product description is required.'
        if not category:
            errors['category'] = 'Product category is required.'
        if not condition:
            errors['condition'] = 'Product condition is required.'
            
        if not sku:
            errors['sku'] = 'Product SKU is required.'
        elif Product.objects.exclude(pk=product_id).filter(sku=sku).exists():
            errors['sku'] = 'Product SKU already exists.'    
        
        if not price:
            errors['price'] = 'Product price is required.'
        if not stock:
            errors['stock'] = 'Product stock is required.'
        if not brand_id:
            errors['brand'] = 'Product brand is required.'

        if errors:
            return render(request, 'main/edit_product_page.html', {'product': product, 'brands': brands, 'errors': errors, 'data': request.POST})

        brand = Brand.objects.get(id=brand_id)
        
        product.name = name
        product.description = description
        product.category = category
        product.condition = condition
        product.sku = sku
        product.price = price
        product.stock = stock
        product.brand = brand
        if product_image:
            product.product_image = product_image
        
        product.save()

        messages.success(request, 'Product updated successfully.')
        return redirect('/dashboard/admin/?section=product-management')
    
    return render(request, 'main/edit_product_page.html', {'product': product, 'brands': brands})

@login_required
def delete_product_view(request, product_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')
    
    product = Product.objects.get(id=product_id)
    
    if not product:
        messages.error(request, "Product not found.")
        return redirect('/dashboard/admin/?section=product-management')
    
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('/dashboard/admin/?section=product-management')