from django.contrib import admin
from .models import User, Document, Invoices, InvoiceItem 
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User,UserAdmin)
admin.site.register(Document)
admin.site.register(Invoices)