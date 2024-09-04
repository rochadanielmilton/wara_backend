from django import template

register = template.Library()

@register.filter
def format_with_dots(value):
    try:
        value = int(value)
        return "{:,}".format(value).replace(",", ".")
    except (ValueError, TypeError):
        return value