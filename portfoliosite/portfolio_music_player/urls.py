"""
    This file is used to direct portfolio_music_player urls to their appropriate views.
"""
from django.urls import path
from django.contrib.staticfiles.urls import static
from django.conf import settings
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'music_player'

urlpatterns = [
    path('', views.player, name='player'),
    path('albums/', views.AlbumListView.as_view(), name='albums'),
    path('songs/', views.SongListView.as_view(), name='songs'),
]

urlpatterns = format_suffix_patterns(urlpatterns)


# Addition for using uploaded media as static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
