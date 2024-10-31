"""
    This file is used to direct writing urls to their appropriate views for writing app.
"""
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import static
from django.conf import settings
from . import views

app_name = 'writing'

urlpatterns = [
    path('', views.writing_landing, name='writing_landing'),
    path('category/<int:category_id>', views.writing_category, name='writing_category'),
    path('project/<int:project_id>', views.writing_project, name='writing_project'),
    path('topic_tag/<int:topic_tag_id>', views.writing_topic_tag, name='writing_topic_tag'),
    path('piece/<int:writing_id>', views.writing, name='piece'),
]
"""
    Variable used to direct various urls to their appropriate views. 
"""

# Addition for using uploaded media as static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
