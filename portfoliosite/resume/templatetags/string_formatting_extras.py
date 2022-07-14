"""
    This file creates extra template tags used to format strings.
"""
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def cut_special_chars(value):
    """
        This template tag cuts special characters from strings, making them good
        to use for things like ids when generating pages.
    """
    disallowed_chars = " .'!`~@#$%^&*()_-+={[}]\\|:;<,>./}`\""
    """This variable holds all characters that will be removed in the rendering process"""

    for char in disallowed_chars:
        value = value.replace(char, '')
    return value
