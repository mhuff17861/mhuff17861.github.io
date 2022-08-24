/* @Overview

  This module does the setup work for the music player, implementing
  dynamic layout fixes and retrieving data from the REST API.

*/

/* @function
This function is the top-level setup the runs once data
is retrieved. It runs all other necessary setup functions for the
music player.
*/
function setup_player(albumData) {
  musicPlayer = new MusicPlayer(albumData, on_track_load);
  setup_album_selection(musicPlayer.all_data());
  setup_track_selection(musicPlayer.get_track_list());
  setup_album_download_selection(musicPlayer.all_data())
  setup_track_download_selection(musicPlayer.get_track_list());
  // setup player and play
  setup_player_controls();
  musicPlayer.select_track();
}

/* @function
This function is used to retrieve all the necessary data for
the music player from the REST API. It as called once the JS
file is loaded.
*/
function retrieve_album_data() {
  ALBUM_URL = "albums.json";

  const albumPromise = fetch(ALBUM_URL);
  console.log("collecting album data");

  albumPromise.then((response) => {
    console.log(`Received response: ${response.status}`);
    if (response.status == 200) {
      console.log("Setting Up...");
      const jsonResponse = response.json();
      jsonResponse.then((data) => {
        setup_player(data);
        console.log("Setup Complete.");
      });
    } else {
      alert("Oops! An error occured when loading the music. Please refresh the page or try again later!");
    }
  });
}

/******** Section to run things on load*************/
retrieve_album_data();

//
// /* @var Contains the tag which will hold the album list for the UI. */
// const albumSelectionContainer = document.querySelector("#albumSelection");
// /* @var Contains the tag which will hold the song list for the UI. */
// const trackSelectionContainer = document.querySelector("#trackSelectionScroll");
// /* @var Contains the tag which holds the initiall hidden track and album lists.*/
// const collapseTrackList = document.querySelector("#collapseTrackList");
//
// // Container Controls
//
// /* @var Contains the button used to open track selection.*/
// const trackCollapseOpenBtn = document.querySelector("#trackCollapseOpenBtn");
// /* @var Contains the button used to close track selection.*/
// const trackCollapseCloseBtn = document.querySelector("#trackCollapseCloseBtn");
// // Current track info display
//
// /* @var Contains the img tag that displays currently playing album covers. */
// const albumCover = document.querySelector("#albumCover");
// /* @var Contains the p tag that displays the currently playing song name. */
// const trackName = document.querySelector("#trackName");
// /* @var Contains the p tag that displays the currently playing album name. */
// const albumName = document.querySelector("#albumName");
// /* @var Contains the p tag that displays the currently playing songs playtime. */
// const trackTime = document.querySelector("#trackTime");
//
// // Track controls
//
// /* @var Contains the range input used to perform seeks on the current song. */
// const trackSlider = document.querySelector("#trackSlider");
// /* @var Contains the play/pause button. */
// const playPauseBtn = document.querySelector("#playPauseBtn");
// /* @var Contains the image display for the play/pause button. */
// const playPauseImg = document.querySelector("#playPauseImg");
// /* @var Contains the previous button. */
// const prevBtn = document.querySelector("#prevBtn");
// /* @var Contains the next button. */
// const nextBtn = document.querySelector("#nextBtn");
//
// // Download controls
//
// /* @var Contains the download popup button. */
// const downloadPopupBtn = document.querySelector("#downloadPopupBtn");
// /* @var Contains the file type dropdown selection. */
// const fileTypeSelection = document.querySelector("#fileTypeSelection");
// /* @var Contains the album download dropdown selection. */
// const albumDownloadSelection = document.querySelector("#albumDownloadSelection");
// /* @var Contains the song download dropdown selection. */
// const songDownloadSelection = document.querySelector("#songDownloadSelection");
// /* @var Contains the checkbox to determine whether a single song is being downloaded. */
// const singleSongDownloadCheck = document.querySelector("#singleSongDownloadCheck");
// /* @var Contains the download confirmation button. */
// const downloadConfirmationBtn = document.querySelector("#downloadConfirmationBtn");
