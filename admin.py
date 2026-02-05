# vendors/admin.py
from django.contrib import admin
from .models import Vendor, ProductTracking

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'status', 'tracking_id', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['company_name', 'tracking_id']

@admin.register(ProductTracking)
class ProductTrackingAdmin(admin.ModelAdmin):
    list_display = ['tracking_id', 'vendor', 'product_name', 'status', 'updated_at']
    list_filter = ['status', 'updated_at']
