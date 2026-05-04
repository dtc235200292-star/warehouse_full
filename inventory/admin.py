from django.contrib import admin
from .models import Category, Supplier, Product, Order, StockHistory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "address")
    search_fields = ("name", "phone")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sku", "category", "supplier", "quantity", "price", "status", "created_at")
    search_fields = ("name", "sku")
    list_filter = ("category", "supplier", "status")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity", "status", "total_price", "created_at")
    search_fields = ("user__username", "product__name")
    list_filter = ("status", "created_at")


@admin.register(StockHistory)
class StockHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "action", "quantity", "created_at", "note")
    search_fields = ("product__name", "note")
    list_filter = ("action", "created_at")
