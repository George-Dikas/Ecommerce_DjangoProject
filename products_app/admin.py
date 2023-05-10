from django.contrib import admin
from . models import Registered, Category, Product, Order, Contact


@admin.register(Registered)
class RegisteredAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified']
    ordering = ['user']
    search_fields = ['user']
    list_per_page = 10

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    ordering = ['title']
    search_fields = ['title']
    list_per_page = 10

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category']
    ordering = ['title']
    search_fields = ['title', 'category']
    list_per_page = 10

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'firstname', 'lastname', 'email', 'phone', 'created_at', 'status']
    ordering = ['created_at']
    search_fields = ['id_transaction']
    list_per_page = 10

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['subject', 'firstname', 'lastname', 'created_at']
    ordering = ['created_at']
    search_fields = ['subject', 'lastname']
    list_per_page = 10
