/* @Overview

  This module sets up the interaction for the music player
  interface and retrieves album information with the REST API
  which delivers song data.

*/
/***** Player Data Variables **********/
let albumData = false;
let currentAlbumIndex = 0;
let currentSongIndex = 0;
let howlerContainer = false;

/*********** DOM Element Variables ************/
// Containers for selection
const albumSelectionContainer = document.querySelector("#albumSelection");
const trackSelectionContainer = document.querySelector("#trackSelectionScroll");
// Current track info display
const albumCover = document.querySelector("#albumCover");
const trackName = document.querySelector("#trackName");
// Track controls
const trackSlider = document.querySelector("#trackSlider");
const playPauseBtn = document.querySelector("#playPauseBtn");
const prevBtn = document.querySelector("#prevBtn");
const nextBtn = document.querySelector("#nextBtn");

/*********************Helper Functions****************/
function find_song_index_by_id(song_id) {
  // check if song is in current song list
  for (const [index, song] of albumData[currentAlbumIndex].tracks.entries()) {
    if (song.song_info.id == song_id) return index;
  }

  return currentSongIndex;
}

function find_album_index_by_id(album_id) {
  // check if song is in current song list
  for (const [index, album] of albumData.entries()) {
    if (album.id == album_id) return index;
  }

  return currentSongIndex;
}

/************************Music Player Controls***********/
function select_song(song_id = null) {
  // If a song_id was given, means album change. So, do that and get song.
  if (song_id != null) {
    // Double check if album was changed in the view. If so, change album.
    if (albumSelectionContainer.value != albumData[currentAlbumIndex].id) {
      console.log("Mismatch for album from UI, changing currentAlbumIndex.");
      currentAlbumIndex = find_album_index_by_id(albumSelectionContainer.value);
      console.log("Index changed to: ", currentAlbumIndex);
    }

    currentSongIndex = find_song_index_by_id(song_id);
  }
  song = albumData[currentAlbumIndex].tracks[currentSongIndex].song_info;
  console.log("Now playing: ", song.title);

  // remove reference to old song and stop it from playing
  if (howlerContainer){
    if (howlerContainer.playing()) howlerContainer.stop();
    delete howlerContainer;
  }

  howlerContainer = new Howl({
    src: song.song_files
  });

  playPauseBtn.innerHTML = "Pause";
  howlerContainer.play();
}

function play_pause() {
  if (howlerContainer.playing()) {
    howlerContainer.pause();
    playPauseBtn.innerHTML = "Play";
  } else {
    howlerContainer.play();
    playPauseBtn.innerHTML = "Pause";
  }
}

function next_song() {
  if ((currentSongIndex + 1) < albumData[currentAlbumIndex].tracks.length) {
    currentSongIndex++;
  } else {
    currentSongIndex = 0;
  }

  select_song();
}

 function previous_song() {
   if ((currentSongIndex) > 0) {
     currentSongIndex--;
   } else {
     currentSongIndex = albumData[currentAlbumIndex].tracks.length - 1;
   }

   select_song();
 }

 function seek_to(timestamp) {

 }
/***********************Setup Functions***************/
function setup_album_selection(albums) {
  /* @function-doc
  This function is used to setup the album selection dropdown,
  stored in albumSelectionContainer.

  Args:
  ------------

  - albums: A list of albums with at least an id and title attribute.
  */

  // put together the album list
  for (const [index, album] of albums.entries()) {
    let option = document.createElement("option");
    option.setAttribute("value", album.id);
    option.innerHTML = album.title;
    albumSelectionContainer.appendChild(option);

    // if it is the first album, set as selected
    if (index == 0) {
      albumSelectionContainer.value = option.value;
    }
  }

  // add click listener that will run updates when a click happens
  albumSelectionContainer.addEventListener("change", function() {
    let albumID = this.value;
    for (const [index, album] of albumData.entries()) {
      if (album.id == albumID) {
        setup_track_selection(album.tracks);
      }
    }
  });
}

function setup_track_selection(song_list) {
  /* @function-doc
  This function is used to setup the song selection dropdown,
  stored in trackSelectionContainer.

  Args:
  ------------

  - song_list: A list of songs with at least a .song_info.id and
  a .song_info.title attribute.
  */

  // Delete previous elements
  while (trackSelectionContainer.firstChild) {
    trackSelectionContainer.removeChild(trackSelectionContainer.lastChild);
  }

  // Setup new tracks
  for (const [index, song] of song_list.entries()) {
    let li = document.createElement("li");
    li.setAttribute("class", "list-group-item p-0");

    let btn = document.createElement("button");
    btn.setAttribute("class", "w-100 h-100 bg-info text-light text-start p-2");
    btn.setAttribute("type", "button");
    btn.setAttribute("value", song.song_info.id);
    btn.innerHTML = song.song_info.title;
    btn.addEventListener("click", function() {
      select_song(this.value);
    });

    li.appendChild(btn);
    trackSelectionContainer.appendChild(li);
  }
}

function setup_controls() {
  /* @function-doc
  This function is used to setup the music player controls.
  Currently, that is the play/pause, next, and previous buttons,
  as well as the slider used to seek on the song.
  */

  playPauseBtn.addEventListener("click", play_pause);
  prevBtn.addEventListener("click", previous_song);
  nextBtn.addEventListener("click", next_song);
}

function setup_player() {
  setup_album_selection(albumData);
  setup_track_selection(albumData[0].tracks);
  // setup player and play
  setup_controls();
}

function retrieve_album_data() {
  /* @function-doc
  This function is used to retrieve all the necessary data for
  the music player.
  */
  ALBUM_URL = "albums.json";

  const albumPromise = fetch(ALBUM_URL);
  console.log("collecting album data");

  albumPromise.then((response) => {
    console.log(`Received response: ${response.status}`);
    if (response.status == 200) {
      console.log("Setting Up...");
      const jsonResponse = response.json();
      jsonResponse.then((data) => {
        albumData = data;
        setup_player();
        console.log("Setup Complete.");
      });
    } else {
      alert("Oops! An error occured when loading the music. Please refresh the page or try again later!");
    }
  });
}

/******** Section to run things on load*************/
retrieve_album_data();
