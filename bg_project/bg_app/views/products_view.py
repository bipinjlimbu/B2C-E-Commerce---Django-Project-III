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