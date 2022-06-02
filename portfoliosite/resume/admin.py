from django.contrib import admin
from .models import *

# Setup for Admin Pages

class CV_Line_Inline(admin.StackedInline):
    model = CV_Line
    extra = 1

class CV_Admin(admin.ModelAdmin):
    list_display = ('name', 'priority')

    fieldsets = [
        ('User Info', {'fields': [ 'user_id' ]}),
        ('Category Info', {'fields': ['name', 'priority']})
    ]

    inlines = [CV_Line_Inline]

# *************** Headers stuff
class Page_Header_Admin(admin.ModelAdmin):
    list_display = ('name', 'user_id', 'title')

# Register your models here.
admin.site.register(Page_Header, Page_Header_Admin)
admin.site.register(Project)
admin.site.register(CV_Category, CV_Admin)
