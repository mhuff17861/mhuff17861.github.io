"""
This module holds the models for the portfolio_music_player app.
"""
from django.db import models
import logging
from datetime import date

logger = logging.getLogger(__name__)

# ********** Models ****************
class Album_QuerySet(models.QuerySet):
    """
    Album_QuerySet. Provides functions for common queries on the Albums table.
    """
    def get_released_albums(self):
        """Retrieves all **released** albums ordered by release_date."""
        logger.debug("Retrieving released albums.")
        return self.filter(release_date__lte=date.today()).order_by('release_date')

    def get_albums_with_track_info(self):
        """Retrieves all albums with their associated Track_Number data, ordered by release_date."""
        logger.debug("Retrieving albums with track info.")
        return self.order_by('release_date').prefetch_related('tracks')

    def get_released_albums_with_track_info(self):
        """Retrieves all **released** albums with their associated Track_Number data, ordered by release_date."""
        logger.debug("Retrieving released albums with track info.")
        return self.filter(release_date__lte=date.today()).order_by('release_date').prefetch_related('tracks')

    def get_albums_with_sales_links(self):
        """Retrieves all albums with their associated Track_Number data, ordered by release_date."""
        logger.debug("Retrieving albums with sales link info.")
        return self.order_by('release_date').prefetch_related('sales_links')

    def get_released_albums_with_sales_links(self):
        """Retrieves all albums with their associated Track_Number data, ordered by release_date."""
        logger.debug("Retrieving **released** albums with sales link info.")
        return self.filter(release_date__lte=date.today()).order_by('release_date').prefetch_related('sales_links')

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
    description = models.TextField(max_length=800, blank=True, null=True)
    """Stores the album description"""
    price = models.DecimalField(max_digits=10, decimal_places=2)
    """Stores the album price"""

    albums = Album_QuerySet.as_manager()
    """The accessor for the Album_QuerySet."""

    def __str__(self):
        return self.title

class Song_QuerySet(models.QuerySet):
    """
    Song_QuerySet. Provides functions for common queries on the Songs table.
    """
    def get_songs_with_track_info(self):
        """Retrieves all songs with their associated Track_Number data."""
        logger.debug("Retrieving songs with track info.")
        return self.all().prefetch_related('track_nums')

    def get_songs_with_song_files(self):
        """Retrieves all songs with their associated Song_File data"""
        logger.debug("Retrieving songs with song file info.")
        return self.all().prefetch_related('song_files')

class Song(models.Model):
    """
        Song model. Sets up the basic information needed for a song to be stored and
        displayed. NOTE: To tie a song to an album, you need to set it up with a Track_Number
    """

    title = models.TextField(max_length=400)
    """Stores the title of the song"""
    description = models.TextField(max_length=800, blank=True, null=True)
    """Stores the song description"""
    price = models.DecimalField(max_digits=10, decimal_places=2)
    """Stores the album price"""

    songs = Song_QuerySet.as_manager()
    """The accessor for the Song_QuerySet."""

    def __str__(self):
        return self.title

class Song_File(models.Model):
    """
        Song_File model. Connects one song to many files, using the song_id as a
        foreign key which can be tied to many stored files.
    """

    song_id = models.ForeignKey(Song, related_name='song_files', on_delete=models.CASCADE)
    """Stores song id as foreign key. related_name is song_files"""
    file = models.FileField(upload_to='songs')
    """Stores the actual track file. Type determined by extenstion"""

    def __str__(self):
        return self.file.path

class Track_Number_QuerySet(models.QuerySet):
    """
    Track_Number_QuerySet. Provides functions for common queries on the Track_Numbers table.
    """

    def get_track_numbers_for_album(self, album_id):
        """Retrieves all songs for the given album"""
        return self.filter(album_id__exact=album_id)

class Track_Number(models.Model):
    """
        Track_Numbers model. Ties a song to an album and sets the track number for
        the song in relation to the album. One song can belong to many albums.
    """
    class Meta:
        unique_together = (('song_id', 'album_id'),)

    song_id = models.ForeignKey(Song, related_name='track_nums', on_delete=models.CASCADE)
    """Stores song id as foreign key. related_name is track_nums"""
    album_id = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    """Stores the album id as a foreign key. related_name is tracks"""
    track_num = models.PositiveSmallIntegerField()

    track_numbers = Track_Number_QuerySet.as_manager()
    """The accessor for the Track_Number_QuerySet."""

    def __str__(self):
        return f'Album: {self.album_id}, Song: {self.song_id}, Track Number: {self.track_num}'

class Album_Sales_Link_QuerySet(models.QuerySet):
    """
    Track_Number_QuerySet. Provides functions for common queries on the Track_Numbers table.
    """

    def get_sales_links_for_album(self, album_id):
        """Retrieves all songs for the given album"""
        return self.filter(album_id__exact=album_id)

class Album_Sales_Link(models.Model):
    """
        Links one album to many sales link, allowing many to be displayed
        if a user wants to download the file.
    """

    album_id = models.ForeignKey(Album, related_name='sales_links', on_delete=models.CASCADE)
    """Stores the album id as a foreign key. related_name is sales_links"""
    url = models.TextField(max_length=800)
    """Stores the url that acts as a sales link"""
    url_display = models.TextField(max_length=100, blank=True, null=True)
    """Stores the text that will be displayed for the shown link. Not required."""

    album_sales_links = Album_Sales_Link_QuerySet.as_manager()

    def __str__(self):
        return f'Album: {self.album_id}, URL: {self.url}'
