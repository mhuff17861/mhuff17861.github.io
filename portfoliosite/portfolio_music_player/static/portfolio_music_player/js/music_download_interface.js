// Download controls
let downloadPlayingDuration = null;

/* @var Contains the file type dropdown selection. */
const downloadModal = document.querySelector("#downloadModal");
/* @var Contains the download popup button. */
const downloadPopupBtn = document.querySelector("#downloadPopupBtn");
/* @var Contains the file type dropdown selection. */
const fileTypeSelection = document.querySelector("#fileTypeSelection");
/* @var Contains the album download dropdown selection. */
const albumDownloadSelection = document.querySelector("#albumDownloadSelection");
/* @var Contains the song download dropdown selection. */
const songDownloadSelection = document.querySelector("#songDownloadSelection");
/* @var Contains the song download label. */
const songDownloadSelectionLabel = document.querySelector("#songDownloadSelectionLabel");
/* @var Contains the checkbox to determine whether a single song is being downloaded. */
const albumDownloadCheck = document.querySelector("#singleSongDownloadCheck");
/* @var Contains the download confirmation button. */
const downloadConfirmationBtn = document.querySelector("#downloadConfirmationBtn");
/* @var Contains the download close buttons. */
const downloadCloseBtns = document.querySelectorAll(".dl-close");
/* @var Contains the download confirmation button. */
const downloadCurrentlyPlayingLabel = document.querySelector("#currentlyPlaying");

/*************** Helper Functions *****************/

/* @function
This function takes a file path and returns the file extension.

Args
-------------

- file_path: File path from which the extension will be found.
*/
function get_file_extension(file_path) {
  return file_path.slice(file_path.lastIndexOf('.') + 1, file_path.length);
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

/***************Download View ***************/

function download() {
  if (albumDownloadCheck.checked) {
    console.log("album download");

  } else {
    console.log("single song download");
    let track = musicPlayer.get_track_by_id(songDownloadSelection.value, albumDownloadSelection.value);

    for (file of track.files) {
      // console.log(get_file_extension(file));
      if (get_file_extension(file) == fileTypeSelection.value) {
        // console.log(`downloading file: file`);
        let url = `songs/download/${songDownloadSelection.value}/${fileTypeSelection.value}`;
        window.open(url);
        break;
      }
    }
  }
  download_close();
}

/* @function
This function updates download info when the popup is first shown to
select the current album and currently playing song.
*/
function download_popup() {
  albumDownloadSelection.value = musicPlayer.get_current_album().id;
  setup_track_download_selection(musicPlayer.get_track_list());
  songDownloadSelection.value = musicPlayer.get_current_track().id;
  start_playing_updates();
}

/* @function
This function stops downloadPlayingDuration when the download popup
closes.
*/
function download_close() {
  stop_playing_updates();
}

/* @function
This function updates the "currently playing" display in the download popup
so that the user can always know what is currently playing when they go to download.
*/
function update_currently_playing() {
  downloadCurrentlyPlayingLabel.innerHTML = `Currently playing: ${musicPlayer.get_current_track().title}<br/> From the Album: ${musicPlayer.get_current_album().title}`;
  // console.log("update dl playing");
}

/* @function
This function starts downloadPlayingDuration, which sends updates
to the download section's "currently playing."
*/
function start_playing_updates() {
  if (!downloadPlayingDuration) {
    // console.log("starting dl playing updates");
    downloadPlayingDuration = setInterval(update_currently_playing, 1000);
  }
}

/* @function
This function stops updates from being sent to the download section's
"currently playing." via downloadPlayingDuration.
*/
function stop_playing_updates() {
  if (downloadPlayingDuration) {
    // console.log("stopping dl playing updates");
    clearInterval(downloadPlayingDuration);
    downloadPlayingDuration = null;
  }
}

/* @function
This function shows/hides the song selection dropdown when the
albumDownloadCheck is changed with.
*/
function album_download_update() {
  if (albumDownloadCheck.checked) {
    songDownloadSelection.disabled = true;
    hide(songDownloadSelection);
    hide(songDownloadSelectionLabel);
  } else {
    songDownloadSelection.disabled = false;
    show(songDownloadSelection);
    show(songDownloadSelectionLabel);
  }
}

/* @function
This function updates the UI accordingly when the selected album
is changed
*/
function album_selection_update(selection) {
  let albumID = selection.value;
  for (const [index, album] of musicPlayer.all_data().entries()) {
    if (album.id == albumID) {
      setup_track_download_selection(album.tracks);
    }
  }
}

/************ Download Setup****************/

/* @function
This function is used to setup the album selection dropdown for
downloads.

Args:
------------

- albums: A list of albums with at least a .title, .id attribute.
*/
function setup_album_download_selection(albums) {
  // put together the album list
  for (const [index, album] of albums.entries()) {
    let option = document.createElement("option");
    option.setAttribute("value", album.id);
    option.innerHTML = album.title;
    albumDownloadSelection.appendChild(option);

    // if it is the first album, set as selected
    if (index == 0) {
      albumDownloadSelection.value = option.value;
    }
  }

  // add a change listener to setup the track download selection
  albumDownloadSelection.addEventListener("change", (e) => { album_selection_update(e.target) });

  albumDownloadCheck.addEventListener("change", album_download_update);

  for (const btn of downloadCloseBtns) {
    btn.addEventListener("click", download_close);
  }

  //setup the download_close function when user clicks outside modal
  downloadModal.addEventListener('hidden.bs.modal', download_close);

  downloadPopupBtn.addEventListener("click", download_popup);

  downloadConfirmationBtn.addEventListener("click", download);
}

/* @function
This function is used to setup the track selection dropdown for
downloads. WARNING: Assumes every song on an album has the
same file types available. Note in admin usage somewhere!

Args:
------------

- track_list: A list of songs with at least a .id and
a .title attribute.
*/
function setup_track_download_selection(track_list) {
  let typeList = [];

  // Delete previous elements
  while (songDownloadSelection.firstChild) {
    songDownloadSelection.removeChild(songDownloadSelection.lastChild);
  }
  while (fileTypeSelection.firstChild) {
    fileTypeSelection.removeChild(fileTypeSelection.lastChild);
  }

  // Setup new download tracks
  for (const [index, song] of track_list.entries()) {
    let option = document.createElement("option");
    option.setAttribute("value", song.id);
    option.innerHTML = song.title;
    songDownloadSelection.appendChild(option);
  }

  // get file types
  for (const file of track_list[0].files) {
    // console.log("File found: ", file)
    type = get_file_extension(file);
    // console.log("Type found: ", type)

    if (!typeList.includes(type)) {
      typeList.push(type);
    }
  }

  // Add file types
  for (type of typeList) {
    let option = document.createElement("option");
    option.setAttribute("value", type);
    option.innerHTML = type;
    fileTypeSelection.appendChild(option);
  }

}
