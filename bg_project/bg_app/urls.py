from django.urls import path
from .views.main_view import home_page
from .views.auth_view import register_view, login_view

urlpatterns = [
    path('', home_page, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
]