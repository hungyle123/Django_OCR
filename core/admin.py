from django.contrib import admin
from .models import User, Document, Invoices, InvoiceItem
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User,UserAdmin)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'uploaded_at')
    list_filter = ('status',)

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0
    readonly_fields = ('product_name', 'quantity', 'unit_price', 'total_price')
    can_delete = False

@admin.register(Invoices)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice_no', 'seller', 'date', 'get_total_items')
    
    inlines = [InvoiceItemInline]

    def get_total_items(self, obj):
        return obj.items.count()
    get_total_items.short_description = 'Number of product'