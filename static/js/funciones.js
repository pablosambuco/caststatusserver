var ongoingTouches = [];

function touchStart(evt) {

}

function touchEnd(evt) {
  
}

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
  ws.send(`volume,${cast},${valor}`);
}

function setVolume(cast, valor) {
  var element = document.getElementById(`volume-${cast}`);
  element.value = valor;
  element.style.background = `linear-gradient(to right, var(--acento) ${element.value}%, var(--lineas) ${element.value}%)`;
}

function setTitle(cast, valor) {
  var element = document.getElementById(`title-${cast}`);
  if (element) element.innerHTML = valor;
}
function setSubTitle(cast, valor) {
  var element = document.getElementById(`subtitle-${cast}`);
  if (element) element.innerHTML = valor;
}
function setSeries(cast, valor) {
  var element = document.getElementById(`series-${cast}`);
  if (element) element.innerHTML = valor;
}
function setSeason(cast, valor) {
  var element = document.getElementById(`season-${cast}`);
  if (element) element.innerHTML = valor;
}
function setEpisode(cast, valor) {
  var element = document.getElementById(`episode-${cast}`);
  if (element) element.innerHTML = valor;
}
function setState(cast, valor) {
  var play = document.getElementById(`play-${cast}`);
  var pause = document.getElementById(`pause-${cast}`);

  if (valor == "PLAYING") {
    play.style.display = "none";
    pause.style.display = "inherit";
  } else {
    pause.style.display = "none";
    play.style.display = "inherit";
  }
}

function setImage(cast, valor) {
  var element = document.getElementById(`image-${cast}`);
  if (element) element.style = `background: url(${valor}) 50% 50%`;
}

function setArtist(cast, valor) {
  //var element = document.getElementById(`artist-${cast}`);
  var element = document.getElementById(`subtitle-${cast}`);
  if (element) element.innerHTML = valor;
}
function setAlbum(cast, valor) {
  var element = document.getElementById(`album-${cast}`);
  if (element) element.innerHTML = valor;
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
    f_volumen(cast, this.value);
  };

  slider.addEventListener('touchstart',touchStart, false);        
  slider.addEventListener('touchEnd', touchEnd, false);

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

function atender(message) {
  jsonObject = JSON.parse(message.data);
  atender_recursivo(jsonObject, "");
}

function atender_recursivo(jsonObject, cast) {
  local_cast = cast;
  for (var key in jsonObject) {
    if (key == "cast") {
      local_cast = jsonObject[key];
    }
    if (jsonObject[key] instanceof Object) {
      atender_recursivo(jsonObject[key], local_cast);
    } else {
      switch (key) {
        case "volume":
          setVolume(local_cast, parseFloat(jsonObject[key])*100);
          break;
        case "title":
          setTitle(local_cast, jsonObject[key]);
          break;
        case "subtitle":
          setSubTitle(local_cast, jsonObject[key]);
          break;
        case "series":
          setSeries(local_cast, jsonObject[key]);
          break;
        case "season":
          setSeason(local_cast, jsonObject[key]);
          break;
        case "episode":
          setEpisode(local_cast, jsonObject[key]);
          break;
        case "state":
          setState(local_cast, jsonObject[key]);
          break;
        case "image":
          setImage(local_cast, jsonObject[key]);
          break;
        case "artist":
          setArtist(local_cast, jsonObject[key]);
          break;
        case "album":
          setAlbum(local_cast, jsonObject[key]);
          break;
      }
    }
  }
}
