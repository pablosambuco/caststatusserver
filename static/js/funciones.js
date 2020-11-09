function setVolume(cast, valor) {
  var slider = document.getElementById("volume-" + cast);
  slider.value = valor;
  slider.style.background =
    "linear-gradient(to right, var(--acento) " +
    slider.value +
    "%, var(--lineas) " +
    slider.value +
    "%)";
  slider.oninput = function () {
    this.style.background =
      "linear-gradient(to right, var(--acento) " +
      this.value +
      "%, var(--lineas) " +
      this.value +
      "%)";
  };
}

function setHandlers(cast) {
  var back = document.getElementById("back-" + cast);
  var play = document.getElementById("play-" + cast);
  var pause = document.getElementById("pause-" + cast);
  var forward = document.getElementById("forward-" + cast);

  back.onclick = function () {};
  play.onclick = function () {
    var play = document.getElementById("play-" + cast);
    var pause = document.getElementById("pause-" + cast);    
    play.style.display = "none";      
    pause.style.display = "inherit";
  };
  pause.onclick = function () {
    var play = document.getElementById("play-" + cast);
    var pause = document.getElementById("pause-" + cast);    
    play.style.display = "inherit";
    pause.style.display = "none";  
  };
  forward.onclick = function () {};
}
