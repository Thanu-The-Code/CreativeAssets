from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies the value by the argument."""
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0
    


from django import template

register = template.Library()

@register.filter(name='first_letter')
def first_letter(value):
    if value:
        return value[0]
    else:
        return ''
    
# laviapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def calculate_total(items):
    return sum(item.price * item.quantity for item in items)

