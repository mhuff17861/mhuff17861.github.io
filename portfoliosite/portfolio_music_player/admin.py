"""
    This file sets up admin pages for the portfolio_music_player app,
    so that data can more easily be entered by the user.
"""
from django.contrib import admin
from .models import *

# Setup for Admin pages
class Album_Sales_Link_Inline(admin.StackedInline):
    """Sets up a nestable stacked inline for Album_Sales_Link Model"""
    model = Album_Sales_Link
    extra = 1

class Album_Admin(admin.ModelAdmin):
    """Sets up an admin view for album data with a sales link inline."""
    list_display = ('title', 'release_date')

    fieldsets = [
        ('Starter Info', {'fields': [ 'title', 'type', 'release_date', 'price' ]}),
        ('Extra Display Info', {'fields': ['cover_image', 'description']})
    ]

    inlines = [Album_Sales_Link_Inline]

class Song_File_Inline(admin.StackedInline):
    "Sets up a nestable stacked inline for the Song_File model"
    model = Song_File
    extra = 1

class Track_Number_Inline(admin.StackedInline):
    "Sets up a nestable stacked inline for the Song_File model"
    model = Track_Number
    extra = 1

class Song_Admin(admin.ModelAdmin):
    """
    Sets up the admin view for Song data with
    a Song_File and Track_Number inline
    """
    list_display = ('title', 'price')

    inlines = [Song_File_Inline, Track_Number_Inline]

# Register your models here.
admin.site.register(Album, Album_Admin)
admin.site.register(Song, Song_Admin)
