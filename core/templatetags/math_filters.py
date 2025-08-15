# core/templatetags/math_filters.py
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
    

@register.filter
def split(value, delimiter):
    try:
        return value.split(delimiter)
    except AttributeError:
        return []