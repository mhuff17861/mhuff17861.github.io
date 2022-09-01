"""
    This file renders the proper template for each view in the portfolio_music_player app.
"""
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from portfolio_music_player.models import Album, Song
from portfolio_music_player.serializers import SongSerializer, TrackNumberSerializer, AlbumSerializer, SalesLinkSerializer
from rest_framework import mixins, generics
from rest_framework.decorators import action
from zipfile import ZipFile
import logging
import os
import tempfile

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

    if song:
        for file in song.song_files.all():
            if file_type in file.file.name:
                response = FileResponse(open(file.file.path, 'rb'), as_attachment=True)
                return response

    raise Http404

def download_album(request, id, file_type):
    """Returns the requested album's with the specified type"""
    album = Album.albums.get_album_by_id(id)

    # Make sure the album exists
    if album:

        tracks = album.tracks.all()
        approved_file_type = False

        # Use a temp file so it is deleted after download.
        with tempfile.NamedTemporaryFile(
            prefix=f'{album.title}_{file_type}',
            suffix='.zip') as tmp_f:
            # Check that songs with file_type exist
            for file in tracks[0].song_id.song_files.all():
                if file_type in file.file.name:
                    approved_file_type = True
                    break

            #Collect and zip the files (mayhaps build once and never again?)
            if approved_file_type:
                with ZipFile(tmp_f, 'w', allowZip64=True) as zipf:
                    for track in tracks:
                        for file in track.song_id.song_files.all():
                            if file_type in file.file.name:
                                zipf.write(file.file.path, arcname=file.file.name)

                tmp_f.seek(0)
                response = FileResponse(open(tmp_f.name, 'rb'), as_attachment=True)
                return response

    raise Http404

class AlbumListView(mixins.ListModelMixin, generics.GenericAPIView):
    """Returns all of the Album data for released albums in serialized form"""
    queryset = Album.albums.get_released_albums()
    serializer_class = AlbumSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class SongListView(mixins.ListModelMixin, generics.GenericAPIView):
    """Returns all of the song data for every stored song in serialized form"""
    queryset = Song.songs.all()
    serializer_class = SongSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
