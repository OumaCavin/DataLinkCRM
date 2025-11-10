"""
Customers views for DataLinkCRM.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Customer

@login_required
def index(request):
    """Customer list view."""
    customers = Customer.objects.filter(user=request.user)
    context = {
        'title': 'Customers',
        'customers': customers,
    }
    return render(request, 'customers/index.html', context)

@login_required
def detail(request, customer_id):
    """Customer detail view."""
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)
    context = {
        'title': customer.name,
        'customer': customer,
    }
    return render(request, 'customers/detail.html', context)

@login_required
def create(request):
    """Customer create view."""
    context = {
        'title': 'Add Customer',
    }
    return render(request, 'customers/form.html', context)
