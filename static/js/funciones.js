
function setVolume(cast, valor) {
  var slider = document.getElementById("volume-" + cast);
  slider.value = valor;
  slider.style.background = `linear-gradient(to right, var(--acento) ${slider.value}%, var(--lineas) ${slider.value}%)`;
}

function setHandlers(cast, uuid) {
  var slider = document.getElementById("volume-" + cast);
  var back = document.getElementById("back-" + cast);
  var play = document.getElementById("play-" + cast);
  var pause = document.getElementById("pause-" + cast);
  var forward = document.getElementById("forward-" + cast);

  slider.oninput = function () {
    this.style.background = `linear-gradient(to right, var(--acento) ${this.value}%, var(--lineas) ${this.value}%)`;
  };
  slider.onmouseup = function () {
    var request = new XMLHttpRequest();
    request.open("POST", "/api", false);
    params = `cast=${cast},accion=volumen,paramero=${this.value}`;
    request.send(params);
  };

  back.onclick = function () {
    var request = new XMLHttpRequest();
    request.open("POST", "/api", false);
    params = `cast=${cast},accion=back,parametro=`;
    request.send(params);
  };
  play.onclick = function () {
    var request = new XMLHttpRequest();
    request.open("POST", "/api", false);
    params = `cast=${cast},accion=play,parametro=`;
    request.send(params);

    var play = document.getElementById("play-" + cast);
    var pause = document.getElementById("pause-" + cast);
    play.style.display = "none";
    pause.style.display = "inherit";
  };
  pause.onclick = function () {
    var request = new XMLHttpRequest();
    request.open("POST", "/api", false);
    params = `cast=${cast},accion=pause,parametro=`;
    request.send(params);

    var play = document.getElementById("play-" + cast);
    var pause = document.getElementById("pause-" + cast);
    play.style.display = "inherit";
    pause.style.display = "none";
  };

  forward.onclick = function () {
    var request = new XMLHttpRequest();
    request.open("POST", "/api", false);
    params = `cast=${cast},accion=forward,parametro=`;
    request.send(params);
  };
}

function setState(response) {
  console.log(response);
}
