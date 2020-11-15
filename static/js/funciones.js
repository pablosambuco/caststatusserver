function f_play(cast) {
  ws.send(`play,${cast}`);
}

function f_pause(cast) {
  ws.send(`pause,${cast}`);
}

function f_back(cast) {
  ws.send(`back,${cast}`);
}

function f_forward(cast) {
  ws.send(`forward,${cast}`);
}

function f_volumen(cast, valor) {
  ws.send(`volumen,${cast},${valor}`);
}

function setVolume(cast, valor) {
  var slider = document.getElementById(`volume-${cast}`);
  slider.value = valor;
  slider.style.background = `linear-gradient(to right, var(--acento) ${slider.value}%, var(--lineas) ${slider.value}%)`;
}

function setHandlers(cast, uuid) {
  var slider = document.getElementById(`volume-${cast}`);
  var back = document.getElementById(`back-${cast}`);
  var play = document.getElementById(`play-${cast}`);
  var pause = document.getElementById(`pause-${cast}`);
  var forward = document.getElementById(`forward-${cast}`);

  slider.oninput = function () {
    this.style.background = `linear-gradient(to right, var(--acento) ${this.value}%, var(--lineas) ${this.value}%)`;
  };

  slider.onmouseup = function () {
    f_volumen(cast,this.value);
  };

  back.onclick = function () {
    f_back(cast);
  };

  play.onclick = function () {
    f_play(cast);

    var play = document.getElementById(`play-${cast}`);
    var pause = document.getElementById(`pause-${cast}`);
    play.style.display = "none";
    pause.style.display = "inherit";
  };
  
  pause.onclick = function () {
    f_pause(cast);

    var play = document.getElementById(`play-${cast}`);
    var pause = document.getElementById(`pause-${cast}`);
    play.style.display = "inherit";
    pause.style.display = "none";
  };

  forward.onclick = function () {
    f_forward(cast);
  };
}

function setState(response) {
  console.log(response);
}
