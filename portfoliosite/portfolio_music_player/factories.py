"""
    This file holds data-generation factories used to create test data for the portfolio_music_player
    app, so testing can be as thorough as possible
"""

import factory
from factory.django import DjangoModelFactory
from .models import *
from datetime import datetime, timedelta

ALBUM_TYPE_CHOICES = [x[0] for x in Album.ALBUM_TYPE_CHOICES]

class AlbumFactory(DjangoModelFactory):
    """
    Generates album data.
    """
    class Meta:
        model = "portfolio_music_player.Album"

    title = factory.Faker('word')
    cover_image = factory.django.ImageField(color='blue', width=700, height=500)
    release_date = factory.Faker('date_between',
        start_date=datetime.fromisoformat('2012-09-01'),
        end_date=datetime.fromisoformat('2024-04-01'))
    type = factory.Iterator(ALBUM_TYPE_CHOICES)
    description = factory.Faker('sentence', nb_words=150)
    price = 1.99
