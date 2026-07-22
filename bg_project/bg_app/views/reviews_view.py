from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Product, Review

@login_required
def add_review_view(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if request.user.is_staff:
        messages.error(request, "Staff members cannot add reviews.")
        return redirect('/products/')
    
    if not product:
        messages.error(request, "Product not found.")
        return redirect('/products/')
    
    if Review.objects.filter(customer=request.user, product=product).exists():
        messages.error(request, "You have already reviewed this product.")
        return redirect(f'/products/{product_id}/')
    
    errors = {}
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not rating:
            errors['rating'] = 'Rating is required.'
        elif not (1 <= int(rating) <= 5):
            errors['rating'] = 'Rating must be between 1 and 5.'

        if not comment:
            errors['comment'] = 'Comment is required.'

        if errors:
            return render(request, 'main/add_review_page.html', {'errors': errors, 'data': request.POST, 'product': product})

        review = Review(customer=request.user, product=product, rating=rating, comment=comment)
        review.save()
        
        messages.success(request, 'Review added successfully.')
        return redirect(f'/products/{product_id}/')
    
    return render(request, 'main/add_review_page.html', {'product': product})

@login_required
def edit_review_view(request, review_id):
    review = Review.objects.get(id=review_id)
    
    if not review:
        messages.error(request, "Review not found.")
        return redirect('/dashboard/')
    
    if request.user != review.customer:
        messages.error(request, "You are not authorized to edit this review.")
        return redirect('/dashboard/')
    
    errors = {}
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not rating:
            errors['rating'] = 'Rating is required.'
        elif not (1 <= int(rating) <= 5):
            errors['rating'] = 'Rating must be between 1 and 5.'

        if not comment:
            errors['comment'] = 'Comment is required.'

        if errors:
            return render(request, 'main/edit_review_page.html', {'errors': errors, 'data': request.POST, 'review': review})

        review.rating = rating
        review.comment = comment
        review.save()
        
        messages.success(request, 'Review updated successfully.')
        return redirect(f'/dashboard/?section=my-reviews')
    
    return render(request, 'main/edit_review_page.html', {'review': review})

@login_required
def delete_review_view(request, review_id):
    review = Review.objects.get(id=review_id)
    
    if not review:
        messages.error(request, "Review not found.")
        return redirect('/dashboard/')
    
    if request.user != review.customer and not request.user.is_staff:
        messages.error(request, "You are not authorized to delete this review.")
        return redirect('/dashboard/')
    
    review.delete()
    messages.success(request, 'Review deleted successfully.')
    
    if request.user.is_staff:
        return redirect(f'/dashboard/admin/?section=product-reviews')
    else:
        return redirect(f'/dashboard/?section=my-reviews')