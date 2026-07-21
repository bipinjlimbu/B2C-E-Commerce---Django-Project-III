from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ..models import User

def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('/')
    
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')

        if not username:
            errors['username'] = 'Username is required.'
        if not email:
            errors['email'] = 'Email is required.'
        if not password:
            errors['password'] = 'Password is required.'
        if password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match.'

        if errors:
            return render(request, 'auth/register_page.html', {'errors': errors, 'data': request.POST})
        
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone=phone,
            address=address,
            profile_picture=profile_picture
        )
        user.save()
        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('/login/')
        
    return render(request, 'auth/register_page.html')