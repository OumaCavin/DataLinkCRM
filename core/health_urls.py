"""
Health check URL configuration.
"""
from django.urls import path
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache

def health_check(request):
    """Basic health check endpoint."""
    return JsonResponse({
        'status': 'healthy',
        'message': 'DataLinkCRM is running',
        'version': '1.0.0'
    })

def detailed_health_check(request):
    """Detailed health check with database and cache verification."""
    try:
        # Check database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Check cache
        cache.set('health_check', 'ok', 10)
        cache_result = cache.get('health_check')
        
        health_status = {
            'status': 'healthy',
            'database': 'ok',
            'cache': 'ok' if cache_result == 'ok' else 'error',
            'version': '1.0.0',
            'timestamp': request.timestamp if hasattr(request, 'timestamp') else 'unknown'
        }
        
        return JsonResponse(health_status)
        
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'version': '1.0.0'
        }, status=503)

urlpatterns = [
    path('', health_check, name='health'),
    path('detailed/', detailed_health_check, name='health_detailed'),
]