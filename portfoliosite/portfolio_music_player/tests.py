"""
    This file contains the tests which are used to verify that the resume app's models, views, templates, and
    their respective functions are all operating properly.
"""
from django.test import TestCase, override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import shutil
from datetime import date
import time
from .models import Album, Song, Song_File, Track_Number, Album_Sales_Link
from .factories import *
import factory.random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By #Me too, selenium, me too.
from selenium.webdriver.common.keys import Keys

TEST_DIR = 'test_data'

@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
def setup_data():
    """
        Sets up data that can be used to test every model/view in a development environment.
    """
    NUM_ALBUMS = 15
    """Sets the number of albums to be generated"""
    NUM_SONGS_PER_ALBUM = 12
    """Sets the number of songs to be generated per album"""
    NUM_SALES_LINKS_PER_ALBUM = 3
    """Sets the number of sales links per album"""
    NUM_SONG_FILES_PER_SONG = 2
    """Sets the number of song files to be generated per song"""

    factory.random.reseed_random('My portfolio website 8675309')

    albums = AlbumFactory.create_batch(NUM_ALBUMS)

    for album in albums:
        songs = SongFactory.create_batch(NUM_SONGS_PER_ALBUM)
        AlbumSalesLinkFactory.create_batch(NUM_SALES_LINKS_PER_ALBUM, album_id=album)
        for i, song in enumerate(songs):
            SongFileFactory.create_batch(NUM_SONG_FILES_PER_SONG, song_id=song)
            TrackNumberFactory.create(album_id=album, song_id=song, track_num=i+1)


def tearDownModule():
    """Deletes temporary files made for testing"""
    print("\nDeleting temporary files...\n")
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass

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
            self.assertTrue(album.tracks, msg="get_albums_with_track_info failed to return track info.")

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
            self.assertTrue(album.tracks, msg="get_released_albums_with_track_info failed to return track info.")
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
            self.assertTrue(album.sales_links, msg="get_albums_with_sales_links failed to return track info.")

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
            self.assertTrue(album.sales_links, msg="get_albums_with_sales_links failed to return track info.")
            self.assertLessEqual(album.release_date, date.today(), msg="Album that has not been released yet was returned by get_released_albums_with_sales_links")

    def test_get_album_by_id(self):
        """test the queryset get_album_by_id"""
        albums = Album.albums.all()

        for album in albums:
            id_test = Album.albums.get_album_by_id(album.id)
            self.assertEqual(album.id, id_test.id, msg="get_albums_with_song_files returned the wrong album.")


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
            self.assertTrue(song.track_nums, msg="get_songs_with_track_info failed to return track info.")

    def test_get_songs_with_song_files(self):
        """test the queryset get_songs_with_song_files"""
        songs = Song.songs.get_songs_with_song_files()
        self.assertTrue(songs, msg="get_songs_with_song_files returned nothing.")

        for i, song in enumerate(songs):
            self.assertTrue(song.song_files, msg="get_songs_with_song_files failed to return song files.")

    def test_get_song_by_id(self):
        """test the queryset get_song_by_id"""
        songs = Song.songs.all()

        for song in songs:
            id_test = Song.songs.get_song_by_id(song.id)
            self.assertEqual(song.id, id_test.id, msg="get_songs_with_song_files returned the wrong song.")

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

@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class ChromeMusicPlayerTest(StaticLiveServerTestCase):
    """
    Sets up tests for the music player in the Chrome browser.
    Requires a settings override for dynamic media request to work, given
    that the test storage directory is different.
    """

    @classmethod
    def setUpTestData(cls):
        """
            Data generation for model testing
        """
        setup_data()

    @classmethod
    def setUpClass(cls):
        """Sets up the selenium web driver"""
        super().setUpClass()
        print('Setting up Chrome web driver...\n')
        cls.selenium = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.setUpTestData()

    @classmethod
    def tearDownClass(cls):
        """Tears down the selenium web driver"""
        cls.selenium.quit()
        super().tearDownClass()

    def player_initialized(self, driver):
        """Returns True if player is initialized, false if not"""
        return self.selenium.find_element(by=By.ID, value='trackName').text != 'Loading...'

    def get_track_title(self, qs, index):
        return qs[0].tracks.all()[index].song_id.title

    def test_base_controls(self):
        """Test the play, pause, next, previous, and scan controls"""
        self.selenium.get(f'{self.live_server_url}/music/')

        initialized = WebDriverWait(self.selenium, timeout=10).until(self.player_initialized)

        if initialized:
            play_btn = self.selenium.find_element(by=By.ID, value='playPauseBtn')
            next_btn = self.selenium.find_element(by=By.ID, value='nextBtn')
            prev_btn = self.selenium.find_element(by=By.ID, value='prevBtn')
            track_slider = self.selenium.find_element(by=By.ID, value='trackSlider')
            track_name = self.selenium.find_element(by=By.ID, value='trackName')
            album_name = self.selenium.find_element(by=By.ID, value='albumName')
            albums = Album.albums.get_released_albums_with_track_info()

            # Used to decide slice index for testing album and track titles
            # View currently adds Album: and Track: to the front of titles
            album_slice = 7
            track_slice = 7

            # Wait times between interactions
            wait = 2

            # Initial setup check
            self.assertEqual(album_name.text[album_slice:], albums[0].title, msg='Wrong album name displayed')
            self.assertEqual(track_name.text[track_slice:], self.get_track_title(albums, 0), msg='Wrong track name displayed')

            # It won't press buttons not in view so enjoy the bad scroll hack :)
            self.selenium.execute_script('window.scrollBy(0,250)')

            #initial play check
            time.sleep(wait)
            play_btn.click()
            time.sleep(wait)
            self.assertTrue(self.selenium.execute_script('return musicPlayer.playing()'), msg='Music player did not start playing')

            # Next Check
            next_btn.click()
            time.sleep(wait)
            self.assertEqual(album_name.text[album_slice:], albums[0].title, msg='Wrong album name displayed after next button pressed')
            self.assertEqual(track_name.text[track_slice:], self.get_track_title(albums, 1), msg='Wrong track name displayed after next button pressed')
            self.assertTrue(self.selenium.execute_script('return musicPlayer.playing()'), msg='Music player did not start playing after next button pressed')

            # Previous Check
            prev_btn.click()
            time.sleep(wait)
            self.assertEqual(album_name.text[album_slice:], albums[0].title, msg='Wrong album name displayed after previous button pressed')
            self.assertEqual(track_name.text[track_slice:], self.get_track_title(albums, 0), msg='Wrong track name displayed after previous button pressed')
            self.assertTrue(self.selenium.execute_script('return musicPlayer.playing()'), msg='Music player did not start playing after previous button pressed')

            # Previous first to last track check
            prev_btn.click()
            time.sleep(wait)
            self.assertEqual(album_name.text[album_slice:], albums[0].title, msg='Wrong album name displayed after previous button pressed while playing first track')
            self.assertEqual(track_name.text[track_slice:], self.get_track_title(albums, len(albums[0].tracks.all())-1), msg='Wrong track name displayed after previous button pressed while playing first track')
            self.assertTrue(self.selenium.execute_script('return musicPlayer.playing()'), msg='Music player did not start playing after previous button pressed while playing first track')

            # Next last to first track check
            next_btn.click()
            time.sleep(wait)
            self.assertEqual(album_name.text[album_slice:], albums[0].title, msg='Wrong album name displayed after next button pressed while playing last track')
            self.assertEqual(track_name.text[track_slice:], self.get_track_title(albums, 0), msg='Wrong track name displayed after next button pressed while playing last track')
            self.assertTrue(self.selenium.execute_script('return musicPlayer.playing()'), msg='Music player did not start playing after next button pressed  while playing last track')

            # Seek Check
            seek_check = float(track_slider.get_attribute('value'))
            for i in range(10):
                track_slider.send_keys(Keys.RIGHT)

            time.sleep(wait)
            self.assertGreater(float(track_slider.get_attribute('value')), seek_check, msg='Track slider did not react to input')
            self.assertGreater(self.selenium.execute_script('return musicPlayer.seek()'), seek_check, msg='Music player did not seek when track slider was interacted with')

            # Auto next check
            for i in range(self.selenium.execute_script('return musicPlayer.duration()') - 10):
                track_slider.send_keys(Keys.RIGHT)

            time.sleep(wait)

            self.assertEqual(album_name.text[album_slice:], albums[0].title, msg='Album changed when the next song was automatically played')
            self.assertEqual(track_name.text[track_slice:], self.get_track_title(albums, 1), msg='Wrong track name displayed after a song was completed and the next song was autoplayed')
            self.assertTrue(self.selenium.execute_script('return musicPlayer.playing()'), msg='Music player did not start playing after the previous song was completed')

        else:
            self.assertTrue(False, msg='Music player never initialized')


    def test_track_list(self):
        """Test the track list display and interaction"""
        pass

    def test_download(self):
        """Test the download UI and functionality"""
        pass

@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class FirefoxMusicPlayerTest(StaticLiveServerTestCase):
    """
    Sets up tests for the music player in the Firefox browser.
    Requires a settings override for dynamic media request to work, given
    that the test storage directory is different.
    """

    @classmethod
    def setUpClass(cls):
        """Sets up the selenium web driver"""
        super().setUpClass()
        cls.selenium = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))


    @classmethod
    def tearDownClass(cls):
        """Tears down the selenium web driver"""
        cls.selenium.quit()
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        """
            Data generation for model testing
        """
        setup_data()
