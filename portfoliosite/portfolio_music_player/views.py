"""
    This file renders the proper template for each view in the portfolio_music_player app.
"""
from django.shortcuts import render
from django.http import HttpResponse
import logging
from portfolio_music_player.models import Album, Song
from portfolio_music_player.serializers import SongSerializer, TrackNumberSerializer, AlbumSerializer, SalesLinkSerializer
from rest_framework import mixins
from rest_framework import generics

logger = logging.getLogger(__name__)

# Create your views here.

# Views
def player(request):
    """Returns the music player with the music_player template."""
    logger.debug(f'Retrieving player view.')
    return render(request, 'portfolio_music_player/music_player.html')

class AlbumListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Album.albums.get_released_albums()
    serializer_class = AlbumSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class SongListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Song.songs.all()
    serializer_class = SongSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
