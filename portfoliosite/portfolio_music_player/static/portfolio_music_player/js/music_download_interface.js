// Download controls

/* @var Contains the download popup button. */
const downloadPopupBtn = document.querySelector("#downloadPopupBtn");
/* @var Contains the file type dropdown selection. */
const fileTypeSelection = document.querySelector("#fileTypeSelection");
/* @var Contains the album download dropdown selection. */
const albumDownloadSelection = document.querySelector("#albumDownloadSelection");
/* @var Contains the song download dropdown selection. */
const songDownloadSelection = document.querySelector("#songDownloadSelection");
/* @var Contains the checkbox to determine whether a single song is being downloaded. */
const singleSongDownloadCheck = document.querySelector("#singleSongDownloadCheck");
/* @var Contains the download confirmation button. */
const downloadConfirmationBtn = document.querySelector("#downloadConfirmationBtn");

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

/***************Download View ***************/

function download() {
  if (singleSongDownloadCheck.checked) {
    let tracks = albumData[find_album_index_by_id(albumDownloadSelection.value)].tracks;
    let track = tracks[find_song_index_by_id(songDownloadSelection.value, albumDownloadSelection.value)];

    for (file of track.files) {
      if (get_file_extension(file) == fileTypeSelection.value) {
        //download
      }
    }
  } else {

  }
}

/* @function
This function updates download info when the popup is first shown to
select the current album and currently playing song.
*/
function download_popup() {
  albumDownloadSelection.value = musicPlayer.get_current_album().id;
  setup_track_download_selection(musicPlayer.get_track_list());
  songDownloadSelection.value = musicPlayer.get_current_track().id;
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
  albumDownloadSelection.addEventListener("change", function() {
    let albumID = this.value;
    for (const [index, album] of musicPlayer.all_data().entries()) {
      if (album.id == albumID) {
        setup_track_download_selection(album.tracks);
      }
    }
  });

  downloadPopupBtn.addEventListener("click", download_popup);
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
