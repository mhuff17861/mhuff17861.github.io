/* @Overview

  This module sets up the interaction for the music player
  interface and retrieves album information with the REST API
  which delivers song data.

  TODO: Min: Show Track Time. Add Album Name Display. Change Play/Next to images. DOCUMENT.
  Max: Allow Downloads. Add sales links.
*/
/***** Player Data Variables **********/
let albumData = false;
let currentAlbumIndex = 0;
let currentSongIndex = 0;
let howlerContainer = false;
let durationInterval;

/*********** DOM Element Variables ************/
// Containers for selection
const albumSelectionContainer = document.querySelector("#albumSelection");
const trackSelectionContainer = document.querySelector("#trackSelectionScroll");
// Current track info display
const albumCover = document.querySelector("#albumCover");
const trackName = document.querySelector("#trackName");
const albumName = document.querySelector("#albumName");
const trackTime = document.querySelector("#trackTime");
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

function timestamp_formatting(seconds) {
  let stamp = new Date(seconds * 1000).toISOString().slice(11, 19);

  if (stamp.charAt(0) == '0' && stamp.charAt(1) == 0) {
    stamp = stamp.slice(3, stamp.length);
  }

  return stamp;
}
/************************Music Player Controls***********/
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

  playPauseBtn.innerHTML = "Pause";
}

function on_howler_load() {
  set_album_info();
  set_track_name();
  update_track_timestamp(0);
  reset_slider_values();
}

function play_pause() {
  if (howlerContainer.playing()) {
    howlerContainer.pause();
    playPauseBtn.innerHTML = "Play";
    stop_seek_updates()
  } else {
    howlerContainer.play();
    playPauseBtn.innerHTML = "Pause";
    start_seek_updates();
  }
}

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

function seek_to(timestamp) {
  if (howlerContainer && howlerContainer.state() == "loaded") {
    // console.log("Seeking to: ", timestamp);
    howlerContainer.seek(timestamp);
  }
}

function reset_slider_values() {
  // console.log("Resetting Slider Values.");
  trackSlider.max = howlerContainer.duration();
  trackSlider.min = 0;
  trackSlider.value = 0;
  trackSlider.step = 1;
  start_seek_updates();
}

function update_seek_tracking() {
  // console.log("Updating slider position to: ", howlerContainer.seek());
  trackSlider.value = howlerContainer.seek();
  update_track_timestamp(trackSlider.value);
}

function start_seek_updates() {
  if (!durationInterval) {
    // console.log("starting slider updates");
    durationInterval = setInterval(update_seek_tracking, 1000);
  }
}

function stop_seek_updates() {
  if (durationInterval) {
    // console.log("stopping slider updates");
    clearInterval(durationInterval);
    durationInterval = null;
  }
}

/*************** Music Player View setup*************/
function set_album_info() {
  albumCover.setAttribute("src", albumData[currentAlbumIndex].cover_image);
  albumName.innerHTML = `Album: ${albumData[currentAlbumIndex].title}`;
}

function set_track_name() {
  trackName.innerHTML = `Track: ${albumData[currentAlbumIndex].tracks[currentSongIndex].song_info.title}`;
}

function update_track_timestamp(seconds) {
  let timestamp = `${timestamp_formatting(seconds)}/${timestamp_formatting(howlerContainer.duration())}`;
  trackTime.innerHTML = timestamp;
}

/***********************Initial Setup Functions***************/
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
      if (howlerContainer.state() != "loading") select_song(this.value);
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

  trackSlider.addEventListener("change", (e) => { seek_to(e.target.value); });
  trackSlider.addEventListener("input", (e) => { update_track_timestamp(e.target.value); });
  trackSlider.addEventListener("mousedown", stop_seek_updates);
  trackSlider.addEventListener("mouseup", start_seek_updates);

}

function setup_player() {
  setup_album_selection(albumData);
  setup_track_selection(albumData[0].tracks);
  // setup player and play
  setup_controls();
  set_album_info(albumData[0].cover_image);
  select_song();
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
