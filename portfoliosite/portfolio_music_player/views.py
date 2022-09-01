"""
    This file renders the proper template for each view in the portfolio_music_player app.
"""
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import logging
from portfolio_music_player.models import Album, Song
from portfolio_music_player.serializers import SongSerializer, TrackNumberSerializer, AlbumSerializer, SalesLinkSerializer
from rest_framework import mixins, generics, viewsets, renderers
from rest_framework.decorators import action

logger = logging.getLogger(__name__)

# Create your views here.

# Views
def player(request):
    """Returns the music player with the music_player template."""
    logger.debug(f'Retrieving player view.')
    return render(request, 'portfolio_music_player/music_player.html')

def download_song(request, id, file_type):
    """Returns the requested song file with the specified type"""
    song = Song.songs.get_song_by_id(id)
    for file in song.song_files.all():
        if file_type in file.file.name:
            response = FileResponse(open(file.file.path, 'rb'), as_attachment=True)
            return response
    raise Http404

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

class SongDownloadRenderer(renderers.BaseRenderer):
    """
        Return data as-is. View should supply a Response.
    """
    media_type = ''
    format = ''
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

class SongDownloadView(viewsets.ReadOnlyModelViewSet):
    queryset = Song.songs.all()

    #Two issues: 1. Change way file is gotten 2. Decision on file type. Probs done in renderer
    @action(methods=['get'], detail=True, renderer_classes=(SongDownloadRenderer,))
    def download(self, *args, **kwargs):
        instance = self.get_object()

        # get an open file handle (I'm just using a file attached to the model for this example):
        file_handle = instance.song_files[0].file.open()

        # send file
        response = FileResponse(file_handle, content_type='whatever')
        response['Content-Length'] = instance.song_files[0].file.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.song_files[0].file.name

        return response
