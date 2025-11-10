"""
DataLinkCRM URL Configuration
Main URL configuration for the CRM application.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from core.views import HomeView

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Redirect root to dashboard
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('home/', HomeView.as_view(), name='home'),
    
    # Core functionality
    path('core/', include('core.app_urls')),
    
    # Authentication (AllAuth)
    path('auth/', include('allauth.urls')),
    
    # Main application features
    path('dashboard/', include('dashboard.urls')),
    path('customers/', include('customers.urls')),
    path('projects/', include('projects.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('payments/', include('payments.urls')),
    path('communications/', include('communications.urls')),
    path('analytics/', include('analytics.urls')),
    path('settings/', include('settings.urls')),
    path('widgets/', include('widgets.urls')),
    path('calendar/', include('schedulecal.urls')),
    path('maps/', include('maps.urls')),
    path('reports/', include('reports.urls')),
    
    # API endpoints
    path('api/v1/', include('core.api_urls')),
    
    # Health check
    path('health/', include('core.health_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Django Debug Toolbar (only in development)
    try:
        import debug_toolbar
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    except ImportError:
        pass

# Custom admin site header
admin.site.site_header = "DataLinkCRM Administration"
admin.site.site_title = "DataLinkCRM Admin"
admin.site.index_title = "DataLinkCRM - Professional CRM System by Cavin Otieno"