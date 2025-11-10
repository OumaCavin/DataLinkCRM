"""
Payments views for DataLinkCRM.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Payment

@login_required
def index(request):
    """Payment list view."""
    payments = Payment.objects.filter(user=request.user)
    context = {
        'title': 'Payments',
        'payments': payments,
    }
    return render(request, 'payments/index.html', context)
