"""
    This file holds data-generation factories used to create test data for the portfolio_music_player
    app, so testing can be as thorough as possible

    **NOTE:** The SongFileFactory currently does not generate functioning audio files. They are just for show.
    Updates are planned to create functioning audio files.
"""

import factory
from factory.django import DjangoModelFactory
from .models import *
from datetime import datetime, timedelta
import random

def get_consistent_future_date():
    """
    Returns a date 3 years in the future from when the function is called, ensuring
    date testing will always have a future date
    """
    return datetime.today() + timedelta(days=1096)

ALBUM_TYPE_CHOICES = [x[0] for x in Album.ALBUM_TYPE_CHOICES]

class AlbumFactory(DjangoModelFactory):
    """
    Generates album data.
    """
    class Meta:
        model = "portfolio_music_player.Album"

    title = factory.Faker('sentence', nb_words=4)
    cover_image = factory.django.ImageField(color='blue', width=700, height=500)
    release_date = factory.Faker('date_between',
        start_date=datetime.fromisoformat('2012-09-01'),
        end_date=get_consistent_future_date())
    type = factory.Iterator(ALBUM_TYPE_CHOICES)
    description = factory.Faker('sentence', nb_words=150)
    price = 1.99

class SongFactory(DjangoModelFactory):
    """
    Generates song data.
    """
    class Meta:
        model = "portfolio_music_player.Song"

    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('sentence', nb_words=150)
    price = 0.99

class SongFileFactory(DjangoModelFactory):
    """
    Generates song_file data.
    """

    class Meta:
        model = "portfolio_music_player.Song_File"

    song_id = factory.SubFactory(SongFactory)
    file = factory.django.FileField(
        filename=factory.LazyAttribute(lambda file: f'{file.factory_parent.song_id.title}{[".mp3", ".webm", ".flac"][random.randrange(0,2)]}'))
    # The lambda above allows the filename to be generated from the song title.

class TrackNumberFactory(DjangoModelFactory):
    """
    Generates Track_Number data
    """

    class Meta:
        model = "portfolio_music_player.Track_Number"

    song_id = factory.SubFactory(SongFactory)
    album_id = factory.SubFactory(AlbumFactory)
    track_num = factory.Sequence(lambda n: n)

class AlbumSalesLinkFactory(DjangoModelFactory):
    """
    Generates Album Sales Link data
    """

    class Meta:
        model = "portfolio_music_player.Album_Sales_Link"

    album_id = factory.SubFactory(AlbumFactory)
    url = "https://google.com"
    url_display = factory.Faker('sentence', nb_words=3)
