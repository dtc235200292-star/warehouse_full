from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "quantity", "price")
    search_fields = ("name", "sku")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "product", "quantity", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name",)
