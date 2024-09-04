from django import template

register = template.Library()

@register.filter
def format_miles(value):
    try:
        return "{:,.2f}".format(float(value)).replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return value
