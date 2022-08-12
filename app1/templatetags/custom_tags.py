from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
import html
register = template.Library()


@register.filter
def low(value):
    h = html.parser
    return mark_safe(value)


@register.filter
def first_el(value):
    return value[0]


@register.filter
def last_el(value):
    return value[-1]

@register.filter
def is_in(v2,value):
    if v2 in value:
        return True