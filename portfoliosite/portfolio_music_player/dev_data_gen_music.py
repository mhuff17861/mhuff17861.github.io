"""
    This file is used to quickly setup data for the portfolio_music_player app based on what factory.py can generate.
    It is definitely not perfect, but requires no manual data entry on the part of the developer, meaning that
    non-automated testing can proceed much faster when developing new apps/views/etc.

    **NOTE:** This file currently does not generate functioning audio files. They are just for show.
    Updates are planned to create functioning audio files.

    Usage:
    -------------

    To use, simply run the python script via the django shell.
    ``python manage.py shell < portfolio_music_player/dev_data_gen_music.py``
"""

from portfolio_music_player.factories import *
import factory.random
import os
import logging

logger = logging.getLogger(__name__)

def setup_data():
    """
        Sets up data that can be used to test every model/view in a development environment.
    """
    NUM_ALBUMS = 5
    """Sets the number of albums to be generated"""
    NUM_SONGS_PER_ALBUM = 5
    """Sets the number of songs to be generated per album"""
    NUM_SALES_LINKS_PER_ALBUM = 2
    """Sets the number of sales links per album"""
    NUM_SONG_FILES_PER_SONG = 3
    """Sets the number of song files to be generated per song"""

    # Make sure generation doesn't run for documentation generation.
    if os.environ.get("CI_MAKING_DOCS") is None:
        logger.debug("Generating Music Player development data.")

        factory.random.reseed_random('My portfolio website 8675309')

        albums = AlbumFactory.create_batch(NUM_ALBUMS)

        for album in albums:
            songs = SongFactory.create_batch(NUM_SONGS_PER_ALBUM)
            AlbumSalesLinkFactory.create_batch(NUM_SALES_LINKS_PER_ALBUM, album_id=album)
            for i, song in enumerate(songs):
                SongFileFactory.create_batch(NUM_SONG_FILES_PER_SONG, song_id=song)
                TrackNumberFactory.create(album_id=album, song_id=song, track_num=i+1)
    else:
        logger.debug("Making docs, not generating data.")

setup_data()
