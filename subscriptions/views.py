"""
Subscriptions views for DataLinkCRM.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Subscription

@login_required
def index(request):
    """Subscription list view."""
    subscriptions = Subscription.objects.filter(user=request.user)
    context = {
        'title': 'Subscriptions',
        'subscriptions': subscriptions,
    }
    return render(request, 'subscriptions/index.html', context)
