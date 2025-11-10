"""
Settings views for DataLinkCRM.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Settings view."""
    context = {
        'title': 'Settings',
    }
    return render(request, 'settings/index.html', context)

@login_required
def profile(request):
    """Profile settings view."""
    context = {
        'title': 'Profile Settings',
    }
    return render(request, 'settings/profile.html', context)

@login_required
def quick_actions(request):
    """Quick actions settings view."""
    context = {
        'title': 'Quick Actions',
    }
    return render(request, 'settings/quick_actions.html', context)

@login_required
def notifications(request):
    """Notifications settings view."""
    context = {
        'title': 'Notifications',
    }
    return render(request, 'settings/notifications.html', context)

@login_required
def widgets(request):
    """Widgets settings view."""
    context = {
        'title': 'Dashboard Widgets',
    }
    return render(request, 'settings/widgets.html', context)
