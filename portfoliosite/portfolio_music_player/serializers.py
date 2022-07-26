"""
This module holds the serializers for the API that will allow access
to all necessary album/song information
"""
from rest_framework import serializers
from portfolio_music_player.models import Album, Song, Track_Number, Song_File, Album_Sales_Link

class SongSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize Song data for use with
    the rest_framework. It includes songs_files via a relation
    to give locations of every song file.
    """
    song_files = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = ['id', 'title', 'description', 'price', 'song_files']

    def get_song_files(self, record: Song):
        song_files = record.song_files.all()
        file_list = []

        for file in song_files:
            file_list.append(file.file.url)

        return file_list

class TrackNumberSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize Track_Number data for use with
    the rest_framework. It includes song data via a relation
    to give access to all song data, including files.
    """
    song_info = SongSerializer(read_only=True, source='song_id')

    class Meta:
        model = Track_Number
        fields = ['track_num', 'song_info']

class SalesLinkSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize Album_Sales_Link data for use with
    the rest_framework.
    """
    class Meta:
        model = Album_Sales_Link
        fields = ['album_id', 'url', 'url_display']

class AlbumSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize Album data for use with
    the rest_framework. It includes track information via the
    TrackNumberSerializer and also includes sales via the
    SalesLinkSerializer in the data.
    """
    tracks = TrackNumberSerializer(many=True, read_only=True)
    sales_links = SalesLinkSerializer(many=True, read_only=True)
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ['id', 'title', 'cover_image', 'type', 'release_date', 'description', 'price', 'tracks', 'sales_links']

    def get_cover_image(self, record: Album):
        return record.cover_image.url
