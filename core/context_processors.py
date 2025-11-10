"""
Context processors for DataLinkCRM.
Add common context to all templates.
"""
from django.conf import settings

def global_settings(request):
    """Add global settings to all templates."""
    return {
        'SITE_NAME': 'DataLinkCRM',
        'SITE_DESCRIPTION': 'Professional CRM System by Cavin Otieno',
        'COMPANY_NAME': 'DataLinkCRM',
        'OWNER_NAME': 'Cavin Otieno',
        'OWNER_EMAIL': 'cavin.otieno012@gmail.com',
        'OWNER_PHONE': '+254708101604',
        'OWNER_WHATSAPP': 'wa.me/+254708101604',
        'OWNER_LINKEDIN': 'https://www.linkedin.com/in/cavin-otieno-9a841260/',
        'STRIPE_PUBLISHABLE_KEY': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', ''),
        'MPESA_PHONE': '+254708101604',
        'KENYA_TIMEZONE': 'Africa/Nairobi',
        'DEBUG': settings.DEBUG,
    }