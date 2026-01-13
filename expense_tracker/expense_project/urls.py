from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from expenses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('add/', views.add_expense, name='add_expense'),
    path('list/', views.expense_list, name='expense_list'),
    path('edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]