from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtract the arg from the value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def income_sum(expenses):
    """Calculate sum of income expenses."""
    return sum(exp.amount for exp in expenses if exp.type == 'income')

@register.filter
def expense_sum(expenses):
    """Calculate sum of expense expenses."""
    return sum(exp.amount for exp in expenses if exp.type == 'expense')