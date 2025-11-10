"""
Analytics views for DataLinkCRM.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Analytics view."""
    context = {
        'title': 'Analytics',
    }
    return render(request, 'analytics/index.html', context)
