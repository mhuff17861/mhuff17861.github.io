"""
    This file is used to direct resume urls to their appropriate views.
"""
from django.urls import path
from django.contrib.staticfiles.urls import static
from django.conf import settings
from . import views

app_name = 'resume'

urlpatterns = [
    path('', views.index, name='index'),
    path('projects', views.projects, name='projects'), 
    path('resume', views.resume, name='resume'),
]
"""
    Variable used to direct various urls to their appropriate views. 
"""

# Addition for using uploaded media as static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
