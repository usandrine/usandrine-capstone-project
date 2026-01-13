from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Sum
from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm
from django.utils import timezone

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def home(request):
    # Get date range for this month
    today = timezone.now().date()
    
    # Calculate totals for current month
    expenses = Expense.objects.filter(user=request.user, date__month=today.month, date__year=today.year)
    total_income = expenses.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense
    
    # Recent transactions
    recent_transactions = Expense.objects.filter(user=request.user).order_by('-date')[:10]
    
    # Category breakdown for expenses only
    categories = Category.objects.filter(user=request.user)
    category_data = []
    for category in categories:
        cat_total = expenses.filter(category=category, type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        if cat_total > 0:
            category_data.append({
                'name': category.name,
                'amount': cat_total
            })
    
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'category_data': category_data,
    }
    
    return render(request, 'expenses/home.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('home')
    else:
        form = ExpenseForm()
    
    # Only show categories for the current user
    form.fields['category'].queryset = Category.objects.filter(user=request.user)
    
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    # Filtering
    category_filter = request.GET.get('category')
    type_filter = request.GET.get('type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if category_filter:
        expenses = expenses.filter(category_id=category_filter)
    if type_filter:
        expenses = expenses.filter(type=type_filter)
    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)
    
    categories = Category.objects.filter(user=request.user)
    
    # Calculate totals for filtered results
    income_total = expenses.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expense_total = expenses.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    net_balance = income_total - expense_total
    
    context = {
        'expenses': expenses,
        'categories': categories,
        'income_total': income_total,
        'expense_total': expense_total,
        'net_balance': net_balance,
    }
    return render(request, 'expenses/expense_list.html', context)

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    
    form.fields['category'].queryset = Category.objects.filter(user=request.user)
    
    return render(request, 'expenses/edit_expense.html', {'form': form, 'expense': expense})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('expense_list')
    return render(request, 'expenses/delete_expense.html', {'expense': expense})

@login_required
def manage_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    
    categories = Category.objects.filter(user=request.user)
    return render(request, 'expenses/manage_categories.html', {'form': form, 'categories': categories})

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        # Update expenses with this category to have no category
        Expense.objects.filter(category=category, user=request.user).update(category=None)
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('manage_categories')
    return render(request, 'expenses/delete_category.html', {'category': category})