/* @Overview

  This module sets up the interaction for the music player
  interface and retrieves album information with the REST API
  which delivers song data. It runs retrieve_album_data on load.

  TODO: Min: Accessibility.
  Max: Allow Downloads. Add sales links.
*/

/***** Player Data Variables **********/

/* @var Contains all collected album data. */
let albumData = false;
/* @var Contains the index of the current album. */
let currentAlbumIndex = 0;
/* @var Contains the index of the current song. */
let currentSongIndex = 0;
/* @var Contains the Howl object that is used to play a song. */
let howlerContainer = false;
/* @var Contains the interval that updates the UI as the song plays. */
let durationInterval;

/*********** DOM Element Variables ************/

// Containers for selection

/* @var Contains the tag which will hold the album list for the UI. */
const albumSelectionContainer = document.querySelector("#albumSelection");
/* @var Contains the tag which will hold the song list for the UI. */
const trackSelectionContainer = document.querySelector("#trackSelectionScroll");
/* @var Contains the tag which holds the initiall hidden track and album lists.*/
const collapseTrackList = document.querySelector("#collapseTrackList");

// Current track info display

/* @var Contains the img tag that displays currently playing album covers. */
const albumCover = document.querySelector("#albumCover");
/* @var Contains the p tag that displays the currently playing song name. */
const trackName = document.querySelector("#trackName");
/* @var Contains the p tag that displays the currently playing album name. */
const albumName = document.querySelector("#albumName");
/* @var Contains the p tag that displays the currently playing songs playtime. */
const trackTime = document.querySelector("#trackTime");

// Track controls

/* @var Contains the range input used to perform seeks on the current song. */
const trackSlider = document.querySelector("#trackSlider");
/* @var Contains the play/pause button. */
const playPauseBtn = document.querySelector("#playPauseBtn");
/* @var Contains the image display for the play/pause button. */
const playPauseImg = document.querySelector("#playPauseImg");
/* @var Contains the previous button. */
const prevBtn = document.querySelector("#prevBtn");
/* @var Contains the next button. */
const nextBtn = document.querySelector("#nextBtn");

/*********************Helper Functions****************/

/* @function
This function takes an argument, song_id, and finds the index of the
song it belongs to in albumData based on currentAlbumIndex. If no song
is found, it returns currentSongIndex.

Args
-------------

- song_id - an integer representing the desired song's id
*/
function find_song_index_by_id(song_id) {
  // check if song is in current song list
  for (const [index, song] of albumData[currentAlbumIndex].tracks.entries()) {
    if (song.song_info.id == song_id) return index;
  }

  return currentSongIndex;
}

/* @function
This function takes an argument, album_id, and finds the index of  the
album it belongs to in albumData. If no album is found, it returns
currentAlbumIndex.

Args
-------------

- album_id - an integer representing the desired album's id
*/
function find_album_index_by_id(album_id) {
  // check if song is in current song list
  for (const [index, album] of albumData.entries()) {
    if (album.id == album_id) return index;
  }

  return currentAlbumIndex;
}

/* @function
This function takes an argument, seconds, and converts it to a timestamp
in the format hh:mm:ss. If seconds is less than 3600, the initial hh: is
removed from the timestamp.

Args
-------------

- seconds - an integer representing the number of seconds which should
be converted to a timestamp.
*/
function timestamp_formatting(seconds) {
  let stamp = new Date(seconds * 1000).toISOString().slice(11, 19);

  if (stamp.charAt(0) == '0' && stamp.charAt(1) == 0) {
    stamp = stamp.slice(3, stamp.length);
  }

  return stamp;
}

/************************Music Player Controls***********/

/* @function
This function sets up howlerContainer with a new song and starts
playing it based on currentAlbumIndex and currentSongIndex. If a
song_id argument is provided, the currentAlbumIndex and currentSongIndex
are updated as appropriate based on the album selected by the user and
the song_id given.

Args
----------------

- song_id (*optional*): if given, the function will play the song with
the given id.
*/
function select_song(song_id = null) {
  // Stop the interval from running
  stop_seek_updates();

  // If a song_id was given, means album change. So, do that and get song.
  if (song_id != null) {
    // Double check if album was changed in the view. If so, change album.
    if (albumSelectionContainer.value != albumData[currentAlbumIndex].id) {
      currentAlbumIndex = find_album_index_by_id(albumSelectionContainer.value);
      console.log("Index changed to: ", currentAlbumIndex);
    }

    currentSongIndex = find_song_index_by_id(song_id);
  }

  //set track info
  song = albumData[currentAlbumIndex].tracks[currentSongIndex].song_info;
  console.log("Now playing: ", song.title);

  // remove reference to old song and stop it from playing
  if (howlerContainer){
    if (howlerContainer.playing()) {
      howlerContainer.stop();
    }
    delete howlerContainer;
  }

  howlerContainer = new Howl({
    src: song.song_files,
    autoplay: true,
    onload: on_howler_load,
    onend: next_song
  });

}

/* @function
This function runs all necessary UI updates once howlerContainer loads
a new track.
*/
function on_howler_load() {
  update_album_info();
  update_track_name();
  set_track_timestamp(0);
  set_play_pause_ui(true);
  reset_slider_values();
}

/* @function
This function plays the current song if it was paused or pauses the
song if it was playing and updates the UI accordingly.
*/
function play_pause() {
  if (howlerContainer.playing()) {
    howlerContainer.pause();
    set_play_pause_ui(false);
    stop_seek_updates()
  } else {
    howlerContainer.play();
    set_play_pause_ui(true);
    start_seek_updates();
  }
}

/* @function
This function plays the next song on the currently playing album.
*/
function next_song() {
  if (howlerContainer.state() != "loading") {
    if ((currentSongIndex + 1) < albumData[currentAlbumIndex].tracks.length) {
      currentSongIndex++;
    } else {
      currentSongIndex = 0;
    }

    select_song();
  }
}

/* @function
This function plays the previous song on the currently playing album.
*/
function previous_song() {
  if (howlerContainer.state() != "loading") {
    if ((currentSongIndex) > 0) {
     currentSongIndex--;
    } else {
     currentSongIndex = albumData[currentAlbumIndex].tracks.length - 1;
    }

    select_song();
  }
}

/* @function
This function seeks the track currently loaded in howlerContainer to
the given timestamp.

Args
-------------

- timestamp: an integer variable representing the number of seconds
to which the song should seek to.
*/
function seek_to(timestamp) {
  if (howlerContainer && howlerContainer.state() == "loaded") {
    // console.log("Seeking to: ", timestamp);
    howlerContainer.seek(timestamp);
  }
}

/*************** Music Player View setup*************/
/* @function
This function updates whether the song is playing on the UI.

Args
-----------

- play - a boolean value, true meaning the track is playing, false
meaning that it is not.
*/
function set_play_pause_ui(play) {
  if (play) {
    playPauseImg.src = pauseIconUrl;
    playPauseImg.alt = "pause button image";
  } else {
    playPauseImg.src = playIconUrl;
    playPauseImg.alt = "play button image";
  }
}

/* @function
This function updates the album image on the UI. It does so automatically based
on currentAlbumIndex.
*/
function update_album_info() {
  albumCover.setAttribute("src", albumData[currentAlbumIndex].cover_image);
  albumName.innerHTML = `Album: ${albumData[currentAlbumIndex].title}`;
}

/* @function
This function updates the track name on the UI. It does so automatically based
on currentAlbumIndex and currentSongIndex.
*/
function update_track_name() {
  trackName.innerHTML = `Track: ${albumData[currentAlbumIndex].tracks[currentSongIndex].song_info.title}`;
}

/* @function
This function takes an argument, seconds, and uses that to update
the timestamp shown on the UI, in the format hh:mm:ss.

Args
--------------

- seconds: an integer containing the number of seconds you want the
timestamp represent.
*/
function set_track_timestamp(seconds) {
  let timestamp = `${timestamp_formatting(seconds)}/${timestamp_formatting(howlerContainer.duration())}`;
  trackTime.innerHTML = timestamp;
}


/* @function
This function resets trackSlider's information, changing the
max to match the current song duration, resetting min and value
to 0, and setting step to 1 before restarting seek updates.
*/
function reset_slider_values() {
  // console.log("Resetting Slider Values.");
  trackSlider.max = howlerContainer.duration();
  trackSlider.min = 0;
  trackSlider.value = 0;
  trackSlider.step = 1;
  start_seek_updates();
}

/* @function
This function updates trackSlider's position and the timestamp
based on the value returned by howlerContainer.seek().
*/
function update_seek_tracking() {
  // console.log("Updating slider position to: ", howlerContainer.seek());
  trackSlider.value = howlerContainer.seek();
  set_track_timestamp(trackSlider.value);
}

/* @function
This function starts durationInterval, which sends seek updates
to trackSlider.
*/
function start_seek_updates() {
  if (!durationInterval) {
    // console.log("starting slider updates");
    durationInterval = setInterval(update_seek_tracking, 1000);
  }
}

/* @function
This function stops seek updates from being sent to trackSlider
via durationInterval.
*/
function stop_seek_updates() {
  if (durationInterval) {
    // console.log("stopping slider updates");
    clearInterval(durationInterval);
    durationInterval = null;
  }
}

/***********************Initial Setup Functions***************/
/* @function
This function is used to setup the album selection dropdown,
stored in albumSelectionContainer.

Args:
------------

- albums: A list of albums with at least an .id and .title attribute.
*/
function setup_album_selection(albums) {
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
/* @function
This function is used to setup the song selection dropdown,
stored in trackSelectionContainer.

Args:
------------

- song_list: A list of songs with at least a .song_info.id and
a .song_info.title attribute.
*/
function setup_track_selection(song_list) {
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
      if (howlerContainer.state() != "loading") {
        select_song(this.value);
        var bsCollapse = new bootstrap.Collapse(collapseTrackList, {
          hide: true
        });
      }
    });

    li.appendChild(btn);
    trackSelectionContainer.appendChild(li);
  }
}

/* @function
This function is used to setup the music player controls.
Currently, that is the play/pause, next, and previous buttons,
as well as the slider used to seek on the song.
*/
function setup_controls() {
  playPauseBtn.addEventListener("click", play_pause);
  prevBtn.addEventListener("click", previous_song);
  nextBtn.addEventListener("click", next_song);

  trackSlider.addEventListener("change", (e) => { seek_to(e.target.value); });
  trackSlider.addEventListener("input", (e) => { set_track_timestamp(e.target.value); });
  trackSlider.addEventListener("mousedown", stop_seek_updates);
  trackSlider.addEventListener("mouseup", start_seek_updates);

}

/* @function
This function is the top-level setup the runs once data
is retrieved. It runs all other necessary setup functions for the
music player.
*/
function setup_player() {
  setup_album_selection(albumData);
  setup_track_selection(albumData[0].tracks);
  // setup player and play
  setup_controls();
  update_album_info();
  select_song();
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
