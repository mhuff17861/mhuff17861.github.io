function resizeFix() {
  let el = document.querySelector("#mainPlayerColumn").offsetHeight;
  document.querySelector("#trackSelectionColumn").style.height = el + "px";
}

window.addEventListener('DOMContentLoaded', resizeFix);
window.addEventListener('resize', resizeFix);
