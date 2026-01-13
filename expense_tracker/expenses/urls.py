from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_expense, name='add_expense'),
    path('list/', views.expense_list, name='expense_list'),
    path('edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
]