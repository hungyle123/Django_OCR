from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True, verbose_name='Age')
    full_name = models.CharField(max_length=60, blank=True, verbose_name='Full name')

    def __str__(self):
        return self.username
    
class Document(models.Model):
    STATUS_CHOICE = [('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed'), ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='invoices/', verbose_name='Receipt image')

    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        default='pending',
        verbose_name='Status',
        )
    
    def __str__(self):
        return f"Receipt {self.id} - {self.user.username}"
    
class Invoices(models.Model):
    document = models.OneToOneField(
        'Document',
        on_delete=models.CASCADE,
        related_name='invoice_result',
        verbose_name='Original document',
        )
    
    invoice_no = models.CharField(max_length=20, blank=True, null=True, verbose_name='No of Receipts')
    seller = models.CharField(max_length=255, blank=True, null=True, verbose_name='Unit seller')
    date = models.DateField(blank=True, null=True, verbose_name='Date purchase')

    total_amount = models.DecimalField(
        max_digits=14,      
        decimal_places=2,  
        blank=True, 
        null=True, 
        verbose_name="Total money"
        )
    
    currency = models.CharField(max_length=10, default="VND", verbose_name="Currency")
    raw_text = models.TextField(blank=True, null=True, verbose_name="Raw Text (OCR)")
    details_json = models.TextField(blank=True, null=True, verbose_name="Detail (JSON)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date process OCR")

    def __str__(self):
        return f"Kết quả {self.invoice_no or ('No invoice_no in receipt - ' + str(self.document.id))} ({self.document.user.username})"
