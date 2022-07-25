"""
    This file contains the tests which are used to verify that the resume app's models, views, templates, and
    their respective functions are all operating properly.
"""
from django.test import TestCase
from django.urls import reverse
from datetime import date
from .models import Album, Song, Song_File, Track_Number, Album_Sales_Link
from .factories import *
import factory.random

def setup_data():
    """
        Sets up data that can be used to test every model/view in a development environment.
    """
    NUM_ALBUMS = 20
    """Sets the number of albums to be generated"""
    NUM_SONGS_PER_ALBUM = 15
    """Sets the number of songs to be generated per album"""
    NUM_SALES_LINKS_PER_ALBUM = 4
    """Sets the number of sales links per album"""
    NUM_SONG_FILES_PER_SONG = 3
    """Sets the number of song files to be generated per song"""

    factory.random.reseed_random('My portfolio website 8675309')

    albums = AlbumFactory.create_batch(NUM_ALBUMS)

    for album in albums:
        songs = SongFactory.create_batch(NUM_SONGS_PER_ALBUM)
        AlbumSalesLinkFactory.create_batch(NUM_SALES_LINKS_PER_ALBUM, album_id=album)
        for i, song in enumerate(songs):
            SongFileFactory.create_batch(NUM_SONG_FILES_PER_SONG, song_id=song)
            TrackNumberFactory.create(album_id=album, song_id=song, track_num=i+1)

# Create your tests here.
class ViewNoDataTests(TestCase):
    """Tests views in the portfolio_music_player app without feeding them model data"""

    def setup(self):
        self.client = Client()

    def test_player_no_data_response(self):
        """
            Test the index url for error free page return
        """
        response = self.client.get(reverse('music_player:player'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio_music_player/music_player.html')

class AlbumTests(TestCase):
    """Sets up tests for Album model"""

    @classmethod
    def setUpTestData(cls):
        """
            Data generation for model testing
        """
        setup_data()

    def test_get_released_albums(self):
        """Test the queryset get_released_albums"""
        albums = Album.albums.get_released_albums()
        self.assertTrue(albums, msg="get_released_albums returned nothing.")

        date_test = date.fromisoformat('1920-01-01')
        for i, album in enumerate(albums):
            if i != (albums.count() - 1):
                self.assertGreaterEqual(album.release_date, date_test,
                    msg="Album Queryset get_released_albums returned albums in the wrong order for release_date. Expect oldest first.")
                date_test = album.release_date
            self.assertLessEqual(album.release_date, date.today(), msg="Album that has not been released yet was returned by get_released_albums")

    def test_get_albums_with_track_info(self):
        """Test the queryset get_albums_with_track_info"""
        albums = Album.albums.get_albums_with_track_info()
        self.assertTrue(albums, msg="get_albums_with_track_info returned nothing.")

        date_test = date.fromisoformat('1920-01-01')
        for i, album in enumerate(albums):
            if i != (albums.count() - 1):
                self.assertGreaterEqual(album.release_date, date_test,
                    msg="Album Queryset get_albums_with_track_info  returned albums in the wrong order for release_date. Expect oldest first.")
                date_test = album.release_date
            self.assertTrue(album.track_number_set, msg="get_albums_with_track_info failed to return track info.")

    def test_get_released_albums_with_track_info(self):
        """Test the queryset get_albums_with_track_info"""
        albums = Album.albums.get_released_albums_with_track_info()
        self.assertTrue(albums, msg="get_released_albums_with_track_info returned nothing.")

        date_test = date.fromisoformat('1920-01-01')
        for i, album in enumerate(albums):
            if i != (albums.count() - 1):
                self.assertGreaterEqual(album.release_date, date_test,
                    msg="Album Queryset get_released_albums_with_track_info returned albums in the wrong order for release_date. Expect oldest first.")
                date_test = album.release_date
            self.assertTrue(album.track_number_set, msg="get_released_albums_with_track_info failed to return track info.")
            self.assertLessEqual(album.release_date, date.today(), msg="Album that has not been released yet was returned by get_released_albums_with_track_info")

    def test_get_albums_with_sales_links(self):
        """Test the queryset get_albums_with_sales_links"""
        albums = Album.albums.get_albums_with_sales_links()
        self.assertTrue(albums, msg="get_albums_with_sales_links returned nothing.")

        date_test = date.fromisoformat('1920-01-01')
        for i, album in enumerate(albums):
            if i != (albums.count() - 1):
                self.assertGreaterEqual(album.release_date, date_test,
                    msg="get_albums_with_sales_links returned albums in the wrong order for release_date. Expect oldest first.")
                date_test = album.release_date
            self.assertTrue(album.album_sales_link_set, msg="get_albums_with_sales_links failed to return track info.")

    def test_get_released_albums_with_sales_links(self):
        """Test the queryset get_released_albums_with_sales_links"""
        albums = Album.albums.get_released_albums_with_sales_links()
        self.assertTrue(albums, msg="get_released_albums_with_sales_links returned nothing.")

        date_test = date.fromisoformat('1920-01-01')
        for i, album in enumerate(albums):
            if i != (albums.count() - 1):
                self.assertGreaterEqual(album.release_date, date_test,
                    msg="get_albums_with_sales_links returned albums in the wrong order for release_date. Expect oldest first.")
                date_test = album.release_date
            self.assertTrue(album.album_sales_link_set, msg="get_albums_with_sales_links failed to return track info.")
            self.assertLessEqual(album.release_date, date.today(), msg="Album that has not been released yet was returned by get_released_albums_with_sales_links")

class SongTests(TestCase):
    """Sets up tests for Song model"""

    @classmethod
    def setUpTestData(cls):
        """
            Data generation for model testing
        """
        setup_data()

    def test_get_songs_with_track_info(self):
        """test the queryset get_songs_with_track_info"""
        songs = Song.songs.get_songs_with_track_info()
        self.assertTrue(songs, msg="get_songs_with_track_info returned nothing.")

        for i, song in enumerate(songs):
            self.assertTrue(song.track_number_set, msg="get_songs_with_track_info failed to return track info.")

    def test_get_songs_with_song_files(self):
        """test the queryset get_songs_with_song_files"""
        songs = Song.songs.get_songs_with_song_files()
        self.assertTrue(songs, msg="get_songs_with_song_files returned nothing.")

        for i, song in enumerate(songs):
            self.assertTrue(song.song_file_set, msg="get_songs_with_song_files failed to return song files.")

class TrackNumberTests(TestCase):
    """Sets up tests for Track_Number model"""

    @classmethod
    def setUpTestData(cls):
        """
            Data generation for model testing
        """
        setup_data()

    def test_get_track_numbers_for_album(self):
        albums = Album.albums.all()

        for album in albums:
            tracks = Track_Number.track_numbers.get_track_numbers_for_album(album.id)
            self.assertTrue(tracks, msg="get_track_numbers_for_album failed to return data")
            for track in tracks:
                self.assertEqual(track.album_id.id, album.id, msg="get_track_numbers_for_album retrieved tracks for the wrong album")

class AlbumSalesLinkTests(TestCase):
    """Sets up tests for Album_Sales_link model"""

    @classmethod
    def setUpTestData(cls):
        """
            Data generation for model testing
        """
        setup_data()

    def test_get_sales_links_for_album(self):
        albums = Album.albums.all()

        for album in albums:
            links = Album_Sales_Link.album_sales_links.get_sales_links_for_album(album.id)
            self.assertTrue(links, msg="get_sales_links_for_album failed to return data")
            for link in links:
                self.assertEqual(link.album_id.id, album.id, msg="get_sales_links_for_album retrieved links for the wrong album")
