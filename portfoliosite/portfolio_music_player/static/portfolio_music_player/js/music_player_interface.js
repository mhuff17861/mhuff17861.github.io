/* @Overview

  This module establishes the interface functions needed to update
  the music player's view depending on current track information and user
  interactions.

  It also implements layout fixes via Javascript,
  ensuring that the size of the music player column and the
  track selection column remain relatively the same.

*/

// Containers

/* @var Variable which will contain the music player once data is retrieved */
let musicPlayer = null;
/* @var Variable which will contain the duration interval to update timestamps */
let durationInterval = null;
/* @var Contains the tag which will hold the album list for the UI. */
const albumSelectionContainer = document.querySelector("#albumSelection");
/* @var Contains the tag which will hold the track list for the UI. */
const trackSelectionContainer = document.querySelector("#trackSelectionScroll");
/* @var Contains the tag which holds the initiall hidden track and album lists.*/
const collapseTrackList = document.querySelector("#collapseTrackList");

// Container Controls

/* @var Contains the button used to open track selection.*/
const trackCollapseOpenBtn = document.querySelector("#trackCollapseOpenBtn");
/* @var Contains the button used to close track selection.*/
const trackCollapseCloseBtn = document.querySelector("#trackCollapseCloseBtn");

// Current track info display

/* @var Contains the img tag that displays currently playing album covers. */
const albumCover = document.querySelector("#albumCover");
/* @var Contains the p tag that displays the currently playing track name. */
const trackName = document.querySelector("#trackName");
/* @var Contains the p tag that displays the currently playing album name. */
const albumName = document.querySelector("#albumName");
/* @var Contains the p tag that displays the currently playing tracks playtime. */
const trackTime = document.querySelector("#trackTime");

// Track controls

/* @var Contains the range input used to perform seeks on the current track. */
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

/* @function
This function takes an element and hides it

Args
-------------

- element: the element to hide.
*/
function hide(element) {
  element.classList.add("d-none");
}

/* @function
**assuming it was hidden by the hide function**, this function
takes an element and shows it.

Args
-------------

- element: the element to hide.
*/
function show(element) {
  element.classList.remove("d-none");
}

/*************** Music Player View setup*************/

/* @function
This function updates whether the track is playing on the UI.

**NOTE**: pauseIconUrl and playIconUrl, both used in this function,
are defined in the music_player.html template due to django's ability
to dynamically update urls via the templating system.

Args
-----------

- play - a boolean value, true meaning the track is playing, false
meaning that it is not.
*/
function set_play_pause_ui(play) {
  if (play) {
    playPauseImg.src = pauseIconUrl;
    playPauseImg.alt = "pause button image";
    playPauseBtn.setAttribute("aria-label", "Pause track Button");
  } else {
    playPauseImg.src = playIconUrl;
    playPauseImg.alt = "play button image";
    playPauseBtn.setAttribute("aria-label", "Play track Button");
  }
}

/* @function
This function updates the album image on the UI. It does so automatically based
on currentAlbumIndex.
*/
function update_album_info() {
  albumCover.setAttribute("src", musicPlayer.get_current_album().coverImage);
  albumName.innerHTML = `Album: ${musicPlayer.get_current_album().title}`;
}

/* @function
This function updates the track name on the UI. It does so automatically based
on currentAlbumIndex and currenttrackIndex.
*/
function update_track_name() {
  trackName.innerHTML = `Track: ${musicPlayer.get_current_track().title}`;
}

/* @function
This function shows, hides, and focuses appropriate elements when
the track list is opened or closed for accessibility purposes.

Args
-----------

- open (default=true): A boolean argument, true meaning that the
track list will be opened, false meaning it will be closed.
*/
function track_list_toggle(open) {
  if (open) {
    hide(trackCollapseOpenBtn);
    hide(downloadPopupBtn);
    trackCollapseCloseBtn.focus();
  } else {
    show(trackCollapseOpenBtn);
    show(downloadPopupBtn);
    trackCollapseOpenBtn.focus();
  }
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
  let timestamp = `${timestamp_formatting(seconds)}/${timestamp_formatting(musicPlayer.duration())}`;
  trackTime.innerHTML = timestamp;
}


/* @function
This function resets trackSlider's information, changing the
max to match the current track duration, resetting min and value
to 0, and setting step to 1 before restarting seek updates.
*/
function reset_slider_values() {
  // console.log("Resetting Slider Values.");
  trackSlider.max = musicPlayer.duration();
  trackSlider.min = 0;
  trackSlider.value = 0;
  trackSlider.step = 1;
  set_track_timestamp(0);
}

/************* Interface Updates *********/

/* @function
This function updates trackSlider's position and the timestamp
based on the value returned by howlerContainer.seek().
*/
function update_seek_tracking() {
  // console.log("Updating slider position to: ", howlerContainer.seek());
  let time = musicPlayer.seek()
  set_track_timestamp(time)
  trackSlider.value = time;
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

/* @function
This function runs all necessary UI updates once howlerContainer loads
a new track.
*/
function on_track_load() {
  update_album_info();
  update_track_name();
  reset_slider_values();
}

/* @function
This function runs all necessary UI updates once howlerContainer loads
a new track.
*/
function on_track_play() {
  set_play_pause_ui(true);
  start_seek_updates();
}

/********************** Track Controls ************************/


/* @function
This function plays the current track if it was paused or pauses the
track if it was playing and updates the UI accordingly.
*/
function play_pause() {
  set_play_pause_ui(musicPlayer.play_pause());
}

/* @function
This function plays the next track on the currently playing album.
*/
function next_track() {
  musicPlayer.next_track(on_track_load);
}

/* @function
This function plays the previous track on the currently playing album.
*/
function previous_track() {
  musicPlayer.previous_track(on_track_load);
}

/* @function
This function seeks the track currently loaded in howlerContainer to
the given timestamp.

Args
-------------

- timestamp: an integer variable representing the number of seconds
to which the track should seek to.
*/
function seek_to(timestamp=null) {
  musicPlayer.seek(timestamp);
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

  // add change listener that will run updates when a click happens
  albumSelectionContainer.addEventListener("change", function() {
      setup_track_selection(musicPlayer.get_album_by_id(this.value).tracks);
  });
}

/* @function
This function is used to setup the track selection dropdown,
stored in trackSelectionContainer.

Args:
------------

- track_list: A list of tracks with at least a .track_info.id and
a .track_info.title attribute.
*/
function setup_track_selection(track_list) {
  // Delete previous elements
  while (trackSelectionContainer.firstChild) {
    trackSelectionContainer.removeChild(trackSelectionContainer.lastChild);
  }

  // Setup new tracks
  for (const [index, track] of track_list.entries()) {
    let li = document.createElement("li");
    li.setAttribute("class", "list-group-item p-0");

    let btn = document.createElement("button");
    btn.setAttribute("class", "w-100 h-100 bg-info text-light text-start p-2");
    btn.setAttribute("type", "button");
    btn.setAttribute("value", track.id);
    btn.innerHTML = track.title;
    btn.addEventListener("click", function() {
      musicPlayer.select_track(true, this.value, albumSelectionContainer.value);
      var bsCollapse = new bootstrap.Collapse(collapseTrackList, {
        hide: true
      });
      track_list_toggle(false);
    });

    li.appendChild(btn);
    trackSelectionContainer.appendChild(li);
  }
}

/* @function
This function is used to setup the music player controls.
Currently, that is the play/pause, next, and previous buttons,
as well as the slider used to seek on the track.
*/
function setup_player_controls() {
  playPauseBtn.addEventListener("click", play_pause);
  prevBtn.addEventListener("click", previous_track);
  nextBtn.addEventListener("click", next_track);

  trackSlider.addEventListener("change", (e) => { seek_to(e.target.value); });
  trackSlider.addEventListener("input", (e) => { set_track_timestamp(e.target.value); });
  trackSlider.addEventListener("mousedown", stop_seek_updates);
  trackSlider.addEventListener("mouseup", start_seek_updates);

  trackCollapseOpenBtn.addEventListener("click", () => {track_list_toggle(true)});
  trackCollapseCloseBtn.addEventListener("click", () => {track_list_toggle(false)});
}

/* @function
This function is used to resize the track list dynamically based on
the size of the contained it is in.
*/
function resizeTrackList() {
  const playerHeight = document.querySelector("#playerContainer");
  const trackList = document.querySelector("#trackSelectionScroll");
  const albumSelectionList = document.querySelector("#albumSelectionList");
  const trackCollapseCloseBtn = document.querySelector("#trackCollapseCloseBtn");
  let resizeRatio = 0.8;

  if (window.innerWidth < 550) {
    console.log("Changing resizeRatio")
    resizeRatio = 0.73;
  }

  let resize = (playerHeight.offsetHeight - albumSelectionList.offsetHeight - trackCollapseCloseBtn.offsetHeight) * resizeRatio;
  console.log(`Resizing track list to ${resize}px`);
  trackList.style.height = `${resize}px`;
}

window.addEventListener("load", resizeTrackList);
window.addEventListener("resize", resizeTrackList);
