from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
import html
register = template.Library()


@register.filter
def low(value):
    h = html.parser
    return mark_safe(value)