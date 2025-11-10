"""
Widgets views for DataLinkCRM.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Widgets view."""
    context = {
        'title': 'Widgets',
    }
    return render(request, 'widgets/index.html', context)
