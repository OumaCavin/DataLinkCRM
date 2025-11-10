"""
ScheduleCal views for DataLinkCRM.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Schedule calendar view."""
    context = {
        'title': 'Calendar',
    }
    return render(request, 'schedulecal/index.html', context)