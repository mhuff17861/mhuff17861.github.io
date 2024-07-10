"""
    This file is used to direct writing urls to their appropriate views.
"""
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import static
from django.conf import settings
from . import views

app_name = 'writing'

urlpatterns = [
    path('', views.writing, name='writing'),
    path('poem/<int:poem_id>', views.visual_poetry, name='visual_poetry')
]
"""
    Variable used to direct various urls to their appropriate views. 
"""

# Addition for using uploaded media as static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
