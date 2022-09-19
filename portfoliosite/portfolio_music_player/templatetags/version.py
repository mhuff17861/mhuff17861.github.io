import time
from django import template

register = template.Library()

version = 0

@register.simple_tag
def version():
    return version
