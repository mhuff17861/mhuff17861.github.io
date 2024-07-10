"""
    This file contains the tests which are used to verify that the portfolio_music_player app and
    it's respective functions are all operating properly.
"""
from django.test import TestCase, override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import shutil
import os
import time
import fnmatch
from pathlib import Path
from datetime import date
from .models import Album, Song, Song_File, Track_Number, Album_Sales_Link
from .factories import *
import factory.random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.select import Select
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
class MusicPlayerUIGenericTest(StaticLiveServerTestCase):
    """
    Generic class for UI testing across browsers. Meant to be inherited from.

    Must be given a selenium driver via an overriden setUp function. Additionally,
    the override should call super().setUp() unless the user wants to customize the
    data generation for testing.
    """

    album_slice = 7
    """
        Used to decide slice index for testing album and track titles
        View currently adds Album: to the front of titles
    """
    track_slice = 7
    """
        Used to decide slice index for testing album and track titles
        View currently adds Track: to the front of titles
    """

    wait = 2
    """Wait times between interactions"""

    test_url = ''
    """Url used for testing"""

    selenium = None
    """The variable used to store the selenium driver when inherited"""

    @classmethod
    def setUpClass(cls):
        """Sets up the selenium web driver"""
        super().setUpClass()

        # Get server url
        cls.test_url = f'{cls.live_server_url}/music/'

    def setUp(self):
        setup_data()

    def tearDown(self):
        self.selenium.quit()
        tearDownModule()

    def player_initialized(self, driver):
        """Returns True if player is initialized, false if not"""
        return self.selenium.find_element(by=By.ID, value='trackName').text != 'Loading...'

    def get_track_title(self, qs, album_index, song_index):
        """Gets a track title based on the specified album and song index."""
        return qs[album_index].tracks.all()[song_index].song_id.title

    def get_track_id(self, qs, album_index, song_index):
        """Gets a track id based on the specified album and song index."""
        return qs[album_index].tracks.all()[song_index].song_id.id

    def get_track_files(self, qs, album_index, song_index):
        """Gets a track's file types based on the specified album and song index."""
        return qs[album_index].tracks.all()[song_index].song_id.song_files.all()

    def get_file_extension(self, file_path):
        return file_path[file_path.rfind('.') + 1:]

    def open_test_page(self):
        """Opens the music player page for testing, if not already opened"""
        if self.selenium.current_url != self.test_url:
            self.selenium.get(self.test_url)

    def player_controls_test(self):
        """Test the play, pause, next, previous, and scan controls"""
        self.open_test_page()

        initialized = WebDriverWait(self.selenium, timeout=10).until(self.player_initialized)

        if initialized:
            play_btn = self.selenium.find_element(by=By.ID, value='playPauseBtn')
            next_btn = self.selenium.find_element(by=By.ID, value='nextBtn')
            prev_btn = self.selenium.find_element(by=By.ID, value='prevBtn')
            track_slider = self.selenium.find_element(by=By.ID, value='trackSlider')

            track_name = self.selenium.find_element(by=By.ID, value='trackName')
            album_name = self.selenium.find_element(by=By.ID, value='albumName')

            albums = Album.albums.get_released_albums_with_track_info().reverse()
            
            test_album_index = 0

            # Initial setup check
            self.assertEqual(album_name.text[self.album_slice:], albums[test_album_index].title, msg='Wrong album name displayed')
            self.assertEqual(track_name.text[self.track_slice:], self.get_track_title(albums, test_album_index, 0), msg='Wrong track name displayed')

            # It won't press buttons not in view so enjoy the bad scroll hack :)
            self.selenium.execute_script('window.scrollBy(0,250)')

            #initial play check
            time.sleep(self.wait)
            play_btn.click()
            time.sleep(self.wait)
            self.assertTrue(self.selenium.execute_script('return musicPlayer.playing()'), msg='Music player did not start playing')

            # Next Check
            next_btn.click()
            time.sleep(self.wait)
            self.assertEqual(album_name.text[self.album_slice:], albums[test_album_index].title, msg='Wrong album name displayed after next button pressed')
            self.assertEqual(track_name.text[self.track_slice:], self.get_track_title(albums, test_album_index, 1), msg='Wrong track name displayed after next button pressed')
            self.assertTrue(self.selenium.execute_script('return musicPlayer.playing()'), msg='Music player did not start playing after next button pressed')

            # Previous Check
            prev_btn.click()
            time.sleep(self.wait)
            self.assertEqual(album_name.text[self.album_slice:], albums[test_album_index].title, msg='Wrong album name displayed after previous button pressed')
            self.assertEqual(track_name.text[self.track_slice:], self.get_track_title(albums, test_album_index, 0), msg='Wrong track name displayed after previous button pressed')
            self.assertTrue(self.selenium.execute_script('return musicPlayer.playing()'), msg='Music player did not start playing after previous button pressed')

            # Previous first to last track check
            prev_btn.click()
            time.sleep(self.wait)
            self.assertEqual(album_name.text[self.album_slice:], albums[test_album_index].title, msg='Wrong album name displayed after previous button pressed while playing first track')
            self.assertEqual(track_name.text[self.track_slice:], self.get_track_title(albums, test_album_index, len(albums[test_album_index].tracks.all())-1), msg='Wrong track name displayed after previous button pressed while playing first track')
            self.assertTrue(self.selenium.execute_script('return musicPlayer.playing()'), msg='Music player did not start playing after previous button pressed while playing first track')

            # Next last to first track check
            next_btn.click()
            time.sleep(self.wait)
            self.assertEqual(album_name.text[self.album_slice:], albums[test_album_index].title, msg='Wrong album name displayed after next button pressed while playing last track')
            self.assertEqual(track_name.text[self.track_slice:], self.get_track_title(albums, test_album_index, 0), msg='Wrong track name displayed after next button pressed while playing last track')
            self.assertTrue(self.selenium.execute_script('return musicPlayer.playing()'), msg='Music player did not start playing after next button pressed  while playing last track')

            # Seek Check
            seek_check = float(track_slider.get_attribute('value'))
            for i in range(10):
                track_slider.send_keys(Keys.RIGHT)

            time.sleep(self.wait)
            self.assertGreater(float(track_slider.get_attribute('value')), seek_check, msg='Track slider did not react to input')
            self.assertGreater(self.selenium.execute_script('return musicPlayer.seek()'), seek_check, msg='Music player did not seek when track slider was interacted with')

            # Auto next check
            for i in range(self.selenium.execute_script('return musicPlayer.duration()') - 10):
                track_slider.send_keys(Keys.RIGHT)

            time.sleep(self.wait + 2)

            self.assertEqual(album_name.text[self.album_slice:], albums[test_album_index].title, msg='Album changed when the next song was automatically played')
            self.assertEqual(track_name.text[self.track_slice:], self.get_track_title(albums, test_album_index, 1), msg='Wrong track name displayed after a song was completed and the next song was autoplayed')
            self.assertTrue(self.selenium.execute_script('return musicPlayer.playing()'), msg='Music player did not start playing after the previous song was completed')

        else:
            self.assertTrue(False, msg='Music player never initialized')


    def track_list_test(self):
        """Test the track list display and interaction"""
        self.open_test_page()

        initialized = WebDriverWait(self.selenium, timeout=10).until(self.player_initialized)

        if initialized:
            open_list_btn = self.selenium.find_element(by=By.ID, value='trackCollapseOpenBtn')
            close_list_btn = self.selenium.find_element(by=By.ID, value='trackCollapseCloseBtn')
            track_list = self.selenium.find_element(by=By.ID, value='collapseTrackList')
            track_selection = self.selenium.find_element(by=By.ID, value='trackSelectionScroll')
            album_selection = self.selenium.find_element(by=By.ID, value='albumSelection')

            track_name = self.selenium.find_element(by=By.ID, value='trackName')
            album_name = self.selenium.find_element(by=By.ID, value='albumName')

            albums = Album.albums.get_released_albums_with_track_info().reverse()

            # Test open and close buttons
            open_list_btn.click()
            time.sleep(self.wait)
            self.assertTrue(track_list.is_displayed(), msg='Track list did not open')


            close_list_btn.click()
            time.sleep(self.wait)
            self.assertFalse(track_list.is_displayed(), msg='Track list did not close after hitting close button')

            # Test track selection, same album
            open_list_btn.click()
            time.sleep(self.wait)
            selection_buttons = track_selection.find_elements(By.TAG_NAME, 'button')
            selection_buttons[2].click()
            time.sleep(self.wait)

            self.assertFalse(track_list.is_displayed(), msg='Track list did not close after track selection')
            self.assertEqual(album_name.text[self.album_slice:], albums[0].title, msg='Wrong album name displayed after track selected')
            self.assertEqual(track_name.text[self.track_slice:], self.get_track_title(albums, 0, 2), msg='Wrong track name displayed after track selected')
            self.assertTrue(self.selenium.execute_script('return musicPlayer.playing()'), msg='Music player did not start playing after track selected')

            # Test album selection and track list updates
            open_list_btn.click()
            time.sleep(self.wait)
            album_select_object = Select(album_selection)
            album_select_object.select_by_value(str(albums[1].id))
            time.sleep(self.wait)
            self.assertEqual(albums[1].title, album_select_object.all_selected_options[0].text)

            selection_buttons = track_selection.find_elements(By.TAG_NAME, 'button')

            for i, btn in enumerate(selection_buttons):
                self.assertEqual(btn.text, self.get_track_title(albums, 1, i))

            # Test track selection, different album
            selection_buttons[2].click()
            time.sleep(self.wait)

            self.assertFalse(track_list.is_displayed(), msg='Track list did not close after track selection with different album')
            self.assertEqual(album_name.text[self.album_slice:], albums[1].title, msg='Wrong album name displayed after track selected with different album')
            self.assertEqual(track_name.text[self.track_slice:], self.get_track_title(albums, 1, 2), msg='Wrong track name displayed after track selected with different album')
            self.assertTrue(self.selenium.execute_script('return musicPlayer.playing()'), msg='Music player did not start playing after track selected with different album')
        else:
            self.assertTrue(False, msg='Music player never initialized')

    def download_test(self):
        """Test the download UI and functionality"""
        self.open_test_page()

        initialized = WebDriverWait(self.selenium, timeout=10).until(self.player_initialized)

        if initialized:
            download_open_btn = self.selenium.find_element(by=By.ID, value='downloadPopupBtn')
            download_btn = self.selenium.find_element(by=By.ID, value='downloadConfirmationBtn')
            bottom_close_btn = self.selenium.find_element(by=By.ID, value='bottomCloseBtn')
            top_close_btn = self.selenium.find_element(by=By.ID, value='topCloseBtn')
            album_download_check = self.selenium.find_element(by=By.ID, value='albumDownloadCheck')
            file_type_selection = self.selenium.find_element(by=By.ID, value='fileTypeSelection')
            album_selection = self.selenium.find_element(by=By.ID, value='albumDownloadSelection')
            track_selection = self.selenium.find_element(by=By.ID, value='songDownloadSelection')

            download_popup = self.selenium.find_element(by=By.ID, value='downloadModal')

            albums = Album.albums.get_released_albums_with_track_info()

            # Test open/close
            download_open_btn.click()
            time.sleep(self.wait + 2)

            self.assertTrue(download_popup.is_displayed())

            bottom_close_btn.click()
            time.sleep(self.wait)
            self.assertFalse(download_popup.is_displayed())

            download_open_btn.click()
            time.sleep(self.wait + 2)

            top_close_btn.click()
            time.sleep(self.wait)
            self.assertFalse(download_popup.is_displayed())

            # Test displayed UI Data
            download_open_btn.click()
            time.sleep(self.wait + 2)
            album_selection_object = Select(album_selection)
            track_selection_object = Select(track_selection)
            file_type_selection_object = Select(file_type_selection)

            for i, album in enumerate(album_selection_object.options):
                album_selection_object.select_by_value(str(albums[i].id))
                self.assertEqual(album_selection_object.first_selected_option.text, albums[i].title, msg="Album option does not match associated title")

                # Check File Types
                file_list = self.get_track_files(albums, i, 0)
                for j, file_type in enumerate(file_list):
                    extension = self.get_file_extension(file_type.file.name)
                    file_type_selection_object.select_by_value(extension)
                    self.assertEqual(file_type_selection_object.first_selected_option.text, extension, msg="File type option does not match available files")

                # Check Songs
                for j, track in enumerate(track_selection_object.options):
                    track_selection_object.select_by_value(str(self.get_track_id(albums, i, j)))
                    self.assertEqual(track_selection_object.first_selected_option.text, str(self.get_track_title(albums, i, j)), msg="Track option does not match associated title")

            # Test checkbox
            album_download_check.click()
            self.assertFalse(track_selection.is_displayed(), msg='Track selection still displayed after selecting album download')
            self.assertTrue(album_download_check.get_attribute('checked'), msg='album download checkbox did not respond to being checked')
            album_download_check.click()
            self.assertFalse(album_download_check.get_attribute('checked'), msg='album download checkbox did not respond to being unchecked')
            self.assertTrue(track_selection.is_displayed(), msg='Track selection not displayed after unselecting album download')

            # Test song download
            fname = track_selection_object.first_selected_option.text
            download_path = str(Path.home() / "Downloads")
            download_btn.click()
            time.sleep(self.wait + 2)

            found = False
            for filename in os.listdir(download_path):
                if fnmatch.fnmatch(filename, f'river*'):
                    found = True
                    os.remove(f'{download_path}/{filename}')
                    break

            self.assertTrue(found, msg='Song download failed')

            # Test album download
            download_open_btn.click()
            time.sleep(self.wait + 2)
            album_download_check.click()
            fname = album_selection_object.first_selected_option.text
            download_btn.click()
            time.sleep(self.wait + 2)
            found = False
            for filename in os.listdir(download_path):
                if fnmatch.fnmatch(filename, f'{fname}*'):
                    found = True
                    os.remove(f'{download_path}/{filename}')
                    break

            self.assertTrue(found, msg='Album download failed')

        else:
            self.assertTrue(False, msg='Music player never initialized')


class ChromeMusicPlayerTest(MusicPlayerUIGenericTest):
    """
    Sets up tests for the music player in the Chrome browser, inheriting
    from MusicPlayerUIGenericTest.
    """

    def setUp(self):
        """
            Data generation for model testing
        """
        super().setUp()

        # Setup web driver
        self.selenium = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def test_player_controls(self):
        self.player_controls_test()

    def test_track_list(self):
        self.track_list_test()

    def test_download(self):
        self.download_test()

# class FirefoxMusicPlayerTest(MusicPlayerUIGenericTest):
#     """
#     Sets up tests for the music player in the Firefox browser, inheriting
#     from MusicPlayerUIGenericTest.
#     """
#
#     def setUp(self):
#         """
#             Data generation for model testing
#         """
#         super().setUp()
#
#         # Setup web driver
#         self.selenium = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
#
#     def test_player_controls(self):
#         self.player_controls_test()
#
#     def test_track_list(self):
#         self.track_list_test()
#
#     def test_download(self):
#         self.download_test()
