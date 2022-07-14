"""
This module holds the models for the portfolio_music_player app.
"""
from django.db import models
import logging

# ********** Models ****************
# class Album_QuerySet(models.QuerySet):
#     """
#     Album_QuerySet. Provides functions for common queries on the Albums table.
#     """
#     def get_albums_with_track_info(self):
#         """Retrieves all albums with their associated Track_Number data, ordered by release_date."""
#         logger.debug("Retrieving albums with track info.")
#         self.order_by('release_date').prefetch_related('track_number_set')

class Album(models.Model):
    """
        Album model. Basic information needed for an album
        to be stored and displayed.
    """

    title = models.TextField(max_length=400)
    """Stores the title of the Album"""
    cover_image = models.ImageField(upload_to="albums")
    """Stores the cover image of the album"""
    release_date = models.DateField()
    """Stores the release date of the album. Can be set to the future"""
    ALBUM_TYPE_CHOICES = (
        ('EP', 'EP'),
        ('LP', 'LP'),
        ('S', 'Single'),
        ('A', 'Album'),
        ('C', 'Collection')
    )
    """Choices for what kind of album is being posted"""
    type = models.TextField(choices=ALBUM_TYPE_CHOICES)
    """Stores the type of album release. Limited to ALBUM_TYPE_CHOICES"""
    description = models.TextField(max_length=800)
    """Stores the album description"""
    price = models.DecimalField(max_digits=10, decimal_places=2)
    """Stores the album price"""

class Song(models.Model):
    """
        Song model. Sets up the basic information needed for a song to be stored and
        displayed. NOTE: To tie a song to an album, you need to set it up with a Track_Number
    """

    title = models.TextField(max_length=400)
    """Stores the title of the song"""
    cover_image = models.ImageField(upload_to="albums")
    """Stores the cover image of the song"""
    description = models.TextField(max_length=800)
    """Stores the song description"""
    price = models.DecimalField(max_digits=10, decimal_places=2)
    """Stores the album price"""

class Song_File(models.Model):
    """
        Song_File model. Connects one song to many files, using the song_id as a
        foreign key which can be tied to many stored files.
    """

    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    """Stores song id as foreign key."""
    file = models.FileField(upload_to='songs')
    """Stores the actual track file. Type determined by extenstion"""

class Track_Number(models.Model):
    """
        Track_Numbers model. Ties a song to an album and sets the track number for
        the song in relation to the album. One song can belong to many albums.
    """
    class Meta:
        unique_together = (('song_id', 'album_id'),)

    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    """Stores song id as foreign key."""
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    """Stores the album id as a foreign key"""
    track_num = models.PositiveSmallIntegerField()

class Album_Sales_Link(models.Model):
    """
        Links one album to many sales link, allowing many to be displayed
        if a user wants to download the file.
    """

    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    """Stores the album id as a foreign key"""
    url = models.TextField(max_length=800)
    """Stores the url that acts as a sales link"""
    url_display = models.TextField(max_length=100, blank=True, null=True)
    """Stores the text that will be displayed for the shown link. Not required."""
