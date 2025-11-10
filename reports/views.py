"""
Reports views for DataLinkCRM.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Reports view."""
    context = {
        'title': 'Reports',
    }
    return render(request, 'reports/index.html', context)