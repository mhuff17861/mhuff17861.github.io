/* @Overview

  This module establishes the models used for the music player.

*/

/* @class
This class defines a read-only model for Songs.

Members
-------------

- id - an unique ID for the song
- title - the title of the song
- description - a song description
- price - the price of the song
- songFiles - the files associated with the song for playing
*/
class Song {
  id;
  title;
  description;
  price;
  files;

  constructor(song_json) {
    this.id = song_json.id;
    this.title = song_json.title;
    this.description = song_json.description;
    this.price = song_json.price;
    this.files = song_json.song_files;
  }
}

/* @class
This class defines a read-only model for Albums.

Members
-------------

- id - an unique ID for the song
- title - the title of the song
- description - a song description
- price - the price of the song
- songFiles - the files associated with the song for playing
*/
class Album {
  id;
  title;
  coverImage;
  type;
  releaseDate;
  description;
  price;
  tracks;

  /* @constructor
  This constructor takes in album data in json format and
  formats it properly for use.
  */
  constructor(album_json) {
    this.id = album_json.id;
    this.title = album_json.title;
    this.coverImage = album_json.cover_image;
    this.type = Album.format_type(album_json.type);
    this.releaseDate = album_json.release_date;
    this.description = album_json.description;
    this.price = album_json.price;
    this.tracks = Album.format_tracks(album_json.tracks);
  }

  //**** Static Functions*****

  /* @function
  This static function takes a album type and converts it into a
  human readable form.

  Args
  ---------

  - type - a type as formatted via the REST API.
  */
  static format_type(type) {
    if (type == "S") {
      return "Single";
    } else if (type == "A") {
      return "Album";
    } else if (type == "EP" || type == "LP") {
      return type;
    } else {
      return "Collection";
    }
  }

  /* @function
  This static function takes an album's tracks and converts them into a
  form better setup for the music player.

  Args
  ---------

  - tracks - the album tracks as given by the REST API.
  */
  static format_tracks(tracks) {
    tracks = tracks.sort((a, b) => parseInt(a.track_num) - parseInt(b.track_num));
    let formattedTracks = [];
    for (const track of tracks) {
      formattedTracks.push(new Song(track.song_info));
    }

    return formattedTracks;
  }

  get_track_by_index(index) {
    if (Number.isInteger(index) && index < tracks.length && index >= 0) {
      return tracks[index];
    } else {
      throw new RangeError(`Track does not exist at ${index}`);
    }
  }
}
