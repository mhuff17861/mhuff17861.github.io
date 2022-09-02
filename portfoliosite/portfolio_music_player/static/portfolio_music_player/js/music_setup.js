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
  musicPlayer = new MusicPlayer(albumData, on_track_load, on_track_play);
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
