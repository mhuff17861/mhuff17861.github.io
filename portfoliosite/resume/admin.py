from django.contrib import admin
from .models import *

class CV_Line_Inline(admin.TabularInline):
    model = CV_Line
    extra = 3

# Setup for Admin Pages
class CVAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Category Info', {'fields': ['category_name', 'user_id', 'priority']}),
        ('CV Lines for Category', {'fields': [], 'classes': ['collapse']})
    ]

    inlines = [CV_Line_Inline]

# Register your models here.
admin.site.register(Page_Header)
admin.site.register(Project)
admin.site.register(CV_Category, CVAdmin)
admin.site.register(CV_Sub_Line)
