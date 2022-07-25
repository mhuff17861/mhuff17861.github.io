"""
This module holds the serializers for the API that will allow access
to all necessary album/song information
"""
from rest_framework import serializers
from portfolio_music_player.models import Album, Song, Track_Number, Song_File, Album_Sales_Link

class SongSerializer(serializers.ModelSerializer):
    song_files = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='file'
     )

    class Meta:
        model = Song
        fields = ['id', 'title', 'description', 'price', 'song_files']

class TrackNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track_Number
        fields = ['album_id', 'song_id', 'track_num']

class SalesLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album_Sales_Link
        fields = ['album_id', 'url', 'url_display']

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackNumberSerializer(many=True, read_only=True)
    sales_links = SalesLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'title', 'cover_image', 'type', 'release_date', 'description', 'price', 'tracks', 'sales_links']
