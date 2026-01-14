from django import template

register = template.Library()

@register.filter
def nl_float(value, decimals=1):
    try:
        formatted = f"{float(value):.{decimals}f}"
        return formatted.replace(".", ",")
    except (ValueError, TypeError):
        return value

