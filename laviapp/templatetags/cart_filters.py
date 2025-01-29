from django import template

register = template.Library()

@register.filter
def multiply(price, quantity):
    return price * quantity

@register.simple_tag
def calculate_total(cart):
    return sum(item["price"] * item["quantity"] for item in cart.values())




@register.filter
def calculate_total(cart):
    total = 0
    for item_data in cart.values():
        total += item_data['price'] * item_data['quantity']
    return total

