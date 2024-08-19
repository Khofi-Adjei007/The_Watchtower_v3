from django import template

register = template.Library()

@register.filter(name='in_list')
def in_list(value, arg):
    """Check if value is in the provided comma-separated list."""
    return value in arg.split(',')
