"""
Payment models for DataLinkCRM.
"""
from django.db import models
from django.contrib.auth.models import User
import uuid

class Payment(models.Model):
    """Payment model."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('stripe', 'Credit/Debit Card'),
        ('mpesa', 'M-PESA'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    reference = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
    
    def __str__(self):
        return f"Payment {self.reference} - {self.amount} {self.currency}"
    
    def get_payment_method_display(self):
        methods = {
            'stripe': 'Credit/Debit Card',
            'mpesa': 'M-PESA',
            'bank_transfer': 'Bank Transfer',
            'cash': 'Cash',
            'cheque': 'Cheque',
        }
        return methods.get(self.payment_method, self.payment_method)
    
    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
