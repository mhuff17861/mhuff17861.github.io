/* @Overview

  This file implements a simple layout fixes via Javascript,
  ensuring that the size of the music player column and the
  track selection column remain relatively the same.

*/

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
