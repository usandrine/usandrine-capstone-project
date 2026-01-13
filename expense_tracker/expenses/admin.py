from django.contrib import admin
from .models import Expense, Category

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'type', 'category', 'date', 'user')
    list_filter = ('type', 'category', 'date', 'user')
    search_fields = ('description',)
    date_hierarchy = 'date'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name',)