from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def get_item(dict, key):
    return dict[key]
