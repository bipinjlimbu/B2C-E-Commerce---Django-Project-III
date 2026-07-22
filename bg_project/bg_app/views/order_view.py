from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Brand, Product, Order

@login_required
def dispatch_order_view(request, order_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')
    
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('/dashboard/admin/?section=order-fulfillment')
    
    if order.status != Order.Status.CONFIRMED:
        messages.error(request, "Only confirmed orders can be dispatched.")
        return redirect('/dashboard/admin/?section=order-fulfillment')
    
    order.status = Order.Status.SHIPPING
    order.save()
    
    messages.success(request, f"Order {order.id} has been marked as dispatched.")
    return redirect('/dashboard/admin/?section=order-fulfillment')

@login_required
def deliver_order_view(request, order_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')
    
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('/dashboard/admin/?section=order-fulfillment')
    
    if order.status != Order.Status.SHIPPING:
        messages.error(request, "Only orders that are shipping can be marked as delivered.")
        return redirect('/dashboard/admin/?section=order-fulfillment')
    
    order.status = Order.Status.DELIVERED
    order.save()
    
    messages.success(request, f"Order {order.id} has been marked as delivered.")
    return redirect('/dashboard/admin/?section=order-fulfillment')

@login_required
def order_completed_view(request, order_id):
    if request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')
    
    try:
        order = Order.objects.get(id=order_id, customer=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('/dashboard/?section=pending-orders')
    
    if order.status != Order.Status.DELIVERED:
        messages.error(request, "Only delivered orders can be marked as completed.")
        return redirect('/dashboard/?section=pending-orders')
    
    order.status = Order.Status.COMPLETED
    order.save()
    
    messages.success(request, f"Order {order.id} has been marked as completed.")
    return redirect('/dashboard/?section=pending-orders')