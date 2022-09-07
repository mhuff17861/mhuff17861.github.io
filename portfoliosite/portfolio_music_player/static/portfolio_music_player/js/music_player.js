/* @Overview

  This module contains the MusicPlayer class, which loads in
  a list of albums and provides the functionality to play, pause,
  seek, next/previous, and select tracks based on that data. It requires
  the data fed in to be compatible with the Album class
  (check music_models.js).

  TODO:
  Max: Allow Downloads. Add sales links.
*/

class MusicPlayer {
  howlerContainer;
  onload;
  onplay;
  albumList;
  currentAlbumIndex = 0;
  currentTrackIndex = 0;

  constructor(albums_json, onload, onplay) {
    this.albumList = [];
    for (const album of albums_json) {
      this.albumList.push(new Album(album));
    }
    this.onload = onload;
    this.onplay = onplay;
  }

  /**************** Getters ***************/

  all_data() {
    return this.albumList;
  }

  get_album_by_id(albumID){
    return this.albumList[this.find_album_index_by_id(albumID)];
  }

  get_current_album() {
    return this.albumList[this.currentAlbumIndex];
  }

  get_track_list() {
    return this.albumList[this.currentAlbumIndex].tracks;
  }

  get_track_list_by_id(albumID){
    return this.albumList[this.find_album_index_by_id(albumID)].tracks;
  }

  get_current_track() {
    return this.albumList[this.currentAlbumIndex].tracks[this.currentTrackIndex];
  }

  get_track_by_id(songID, albumID) {
    return this.albumList[this.find_album_index_by_id(albumID)].tracks[this.find_track_index_by_id(songID)]
  }

  duration() {
    if (this.howlerContainer && this.howlerContainer.state() == "loaded") {
      return this.howlerContainer.duration();
    }

    return 0;
  }

  /*************** Setters *********/

  /* @function
  This function seeks the track currently loaded in howlerContainer to
  the given timestamp.

  Args
  -------------

  - timestamp: an integer variable representing the number of seconds
  to which the track should seek to.
  */
  seek(timestamp=null) {
    if (this.howlerContainer && this.howlerContainer.state() == "loaded") {
      // console.log("Seeking to: ", timestamp);

      if (timestamp != null) {
        return this.howlerContainer.seek(timestamp);
      }
      return this.howlerContainer.seek();
    }

    return 0;
  }

  /*************** functionality *********/

  /* @function
  This function sets up howlerContainer with a new track and starts
  playing it based on currentAlbumIndex and currentTrackIndex. If a
  track_id argument is provided, the currentAlbumIndex and currentTrackIndex
  are updated as appropriate based on the album selected by the user and
  the track_id given.

  Args
  ----------------

  - autoplay (*optional*, default=false): boolean deciding whether the
  track will autoplay after selection.
  - track_id (*optional*): if given, the function will play the track with
  the given id.
  - album_id (*optional*): if given, the function will play the track with
  the given id from the given album id.
  */
  select_track(autoplay=false, track_id = null, album_id = null) {
    // If a track_id was given, means album change. So, do that and get track.
    if (track_id != null) {
      // Double check if album was changed in the view. If so, change album.
      if (album_id != null && album_id != this.albumList[this.currentAlbumIndex].id) {
        this.currentAlbumIndex = this.find_album_index_by_id(album_id);
      }

      this.currentTrackIndex = this.find_track_index_by_id(track_id);
    }

    //set track info
    let track = this.albumList[this.currentAlbumIndex].tracks[this.currentTrackIndex];
    console.log("Now playing: ", track.title);

    // remove reference to old track and stop it from playing
    if (this.howlerContainer){
      if (this.howlerContainer.playing()) {
        this.howlerContainer.stop();
      }
      this.howlerContainer = null;
    }

    // do this because "this" in javascript refers to caller not original obj
    let that = this;

    // Check if track array was sorted
    // console.log(`Track File List: ${track.files}`);

    this.howlerContainer = new Howl({
      src: track.files,
      html5: true, //enable streaming
      autoplay: autoplay,
      onload: this.onload,
      onplay: this.onplay,
      onend: () => { return that.next_track() }
    });

    let selection_info = {
      "album_info": this.albumList[this.currentAlbumIndex],
      "track_info": track
    };

    return selection_info;
  }

  /* @function
  This function plays the current track if it was paused or pauses the
  track if it was playing.
  */
  play_pause() {
    if (this.howlerContainer.playing()) {
      this.howlerContainer.pause();
      return false;
    } else {
      this.howlerContainer.play();
      return true;
    }
  }

  /* @function
  This function plays the next track on the currently playing album.
  */
  next_track() {
    if (this.howlerContainer.state() != "loading") {
      if ((this.currentTrackIndex + 1) < this.albumList[this.currentAlbumIndex].tracks.length) {
        this.currentTrackIndex++;
      } else {
        this.currentTrackIndex = 0;
      }

      return this.select_track(true);
    }
  }

  /* @function
  This function plays the previous track on the currently playing album.
  */
  previous_track() {
    if (this.howlerContainer.state() != "loading") {
      if ((this.currentTrackIndex) > 0) {
       this.currentTrackIndex--;
      } else {
       this.currentTrackIndex = this.albumList[this.currentAlbumIndex].tracks.length - 1;
      }

      return this.select_track(true);
    }
  }

  /************* Helpers ************/
  /* @function
  This function takes an argument, track_id, and finds the index of the
  track it belongs to in albumList based on currentAlbumIndex. If no track
  is found, it returns currentTrackIndex.

  Args
  -------------

  - track_id - an integer representing the desired track's id
  - album_id (*optional*) - an integer representing the album id of the album
  in which the track should be searched for.
  */
  find_track_index_by_id(track_id, album_id=null) {
    if (album_id == null) {
      // check if track is in current track list
      for (const [index, track] of this.albumList[this.currentAlbumIndex].tracks.entries()) {
        if (track.id == track_id) return index;
      }
    } else {
      // check if track is in current track list
      for (const [index, track] of this.albumList[this.find_album_index_by_id(album_id)].tracks.entries()) {
        if (track.id == track_id) return index;
      }
    }
    return this.currentTrackIndex;
  }

  /* @function
  This function takes an argument, album_id, and finds the index of  the
  album it belongs to in albumList. If no album is found, it returns
  currentAlbumIndex.

  Args
  -------------

  - album_id - an integer representing the desired album's id
  */
  find_album_index_by_id(album_id) {
    // check if track is in current track list
    for (const [index, album] of this.albumList.entries()) {
      if (album.id == album_id) return index;
    }

    return this.currentAlbumIndex;
  }

  download(window_inst, file_type, album_id, song_id=null) {
      if (song_id == null) {
        // console.log("album download");
        let album = this.get_album_by_id(album_id);
        let url = `albums/download/${album_id}/${file_type}`;
        window_inst.open(url)
      } else {
        // console.log("single song download");
        let track = this.get_track_by_id(songDownloadSelection.value, albumDownloadSelection.value);

        for (const file of track.files) {
          // console.log(Song.get_file_extension(file));
          if (Song.get_file_extension(file) == file_type) {
            // console.log(`downloading file: file`);
            let url = `songs/download/${song_id}/${file_type}`;
            window_inst.open(url);
            break;
          }
        }
      }
  }


}
