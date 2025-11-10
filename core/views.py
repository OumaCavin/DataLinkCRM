"""
Core app views for DataLinkCRM.
"""
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HomeView(TemplateView):
    """Home page view."""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Welcome to DataLinkCRM'
        context['subtitle'] = 'Professional CRM System by Cavin Otieno'
        return context

class DashboardRedirectView(TemplateView):
    """Redirect to dashboard for authenticated users."""
    template_name = 'core/dashboard_redirect.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard Redirect'
        return context

def handler404(request, exception):
    """Custom 404 error handler."""
    return render(request, 'errors/404.html', {
        'title': 'Page Not Found',
        'error': exception,
    })

def handler500(request):
    """Custom 500 error handler."""
    return render(request, 'errors/500.html', {
        'title': 'Server Error',
    })

def handler403(request, exception):
    """Custom 403 error handler."""
    return render(request, 'errors/403.html', {
        'title': 'Permission Denied',
        'error': exception,
    })

def handler400(request, exception):
    """Custom 400 error handler."""
    return render(request, 'errors/400.html', {
        'title': 'Bad Request',
        'error': exception,
    })