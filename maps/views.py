"""
Maps views for DataLinkCRM.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Maps view."""
    context = {
        'title': 'Maps',
    }
    return render(request, 'maps/index.html', context)