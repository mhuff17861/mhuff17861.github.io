from django.contrib import admin
import nested_admin
from .models import *

# Setup for Admin Pages

# ******CV Stuff**********
class CV_Sub_Line_Inline(nested_admin.NestedStackedInline):
    model = CV_Sub_Line
    extra = 0


class CV_Line_Inline(nested_admin.NestedTabularInline):
    model = CV_Line
    extra = 1
    inlines = [CV_Sub_Line_Inline]

class CV_Admin(nested_admin.NestedModelAdmin):
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
