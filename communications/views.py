"""
Communications views for DataLinkCRM.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Communications view."""
    context = {
        'title': 'Communications',
    }
    return render(request, 'communications/index.html', context)
