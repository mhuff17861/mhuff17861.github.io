"""
    This file sets up admin pages for the portfolio_music_player app,
    so that data can more easily be entered by the user.
"""
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Song_File)
admin.site.register(Track_Number)
admin.site.register(Album_Sales_Link)
