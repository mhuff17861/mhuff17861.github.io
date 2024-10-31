"""
    This file sets up admin pages for the resume app, so that data can more
    easily be entered by the user.
"""
from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import *

# Setup for Admin Pages


# Register your models here.
admin.site.register(Author, MarkdownxModelAdmin)
admin.site.register(Writing_Category)
admin.site.register(Writing_Project)
admin.site.register(Writing_Topic_Tag)
admin.site.register(Writing, MarkdownxModelAdmin)