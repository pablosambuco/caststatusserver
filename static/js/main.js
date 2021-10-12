Console = {
    log: function(message) {
        console.log(message);
    }
}

require.config({
  paths: {
    vibrant: "https://cdnjs.cloudflare.com/ajax/libs/vibrant.js/1.0.0/Vibrant",
  },
});

require(["vibrant"], () => {
  Console.log("Vibrant cargado");
});

var ws = "";
var actualizar = "";

Number.prototype.pad = function (size) {
  var s = String(this);
  while (s.length < (size || 2)) {
    s = "0" + s;
  }
  return s;
};

function f_play(cast) {
  ws.send(`play,${cast}`);
}

function f_pause(cast) {
  ws.send(`pause,${cast}`);
}

function f_back(cast) {
  ws.send(`back,${cast}`);
}

function f_back10(cast) {
  ws.send(`back10,${cast}`);
}

function f_forward10(cast) {
  ws.send(`forward10,${cast}`);
}
function f_forward(cast) {
  ws.send(`forward,${cast}`);
}

function f_volumen(cast, valor) {
  ws.send(`volume,${cast},${valor}`);
}

function f_position(cast, valor) {
  ws.send(`position,${cast},${valor}`);
}

function f_mute(cast) {
  ws.send(`mute,${cast}`);
}

function f_unmute(cast) {
  ws.send(`unmute,${cast}`);
}

function setPosition(cast, valor) {
  var element = document.getElementById(`position-${cast}`);
  element.value = valor;
  element.style.background = `linear-gradient(to right, rgb(var(--acento)) ${element.value}%, rgb(var(--lineas)) ${element.value}%)`;
}

function setDuration(cast, valor) {
  var element = document.getElementById(`position-${cast}`);
  element.setAttribute("duration", valor);
}

function setVolume(cast, valor) {
  var element = document.getElementById(`volume-${cast}`);
  element.value = valor;
  element.style.background = `linear-gradient(to right, rgb(var(--acento)) ${element.value}%, rgb(var(--lineas)) ${element.value}%)`;
  if (valor > 0) setMute(cast, false);
  else setMute(cast, true);
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

function setMute(cast, valor) {
  var mute = document.getElementById(`mute-${cast}`);
  var unmute = document.getElementById(`unmute-${cast}`);

  if (valor == true) {
    mute.style.display = "none";
    unmute.style.display = "inherit";
  } else {
    unmute.style.display = "none";
    mute.style.display = "inherit";
  }
}

function setImage(cast, valor) {
  var element = document.getElementById(`image-${cast}`);
  if (element)
    element.style = `background: url(${valor}) 50% 50%; background-size: 450px;`;
}

function setArtist(cast, valor) {
  var element = document.getElementById(`subtitle-${cast}`);
  if (element) element.innerHTML = valor;
}

function setAlbum(cast, valor) {
  var element = document.getElementById(`album-${cast}`);
  if (element) element.innerHTML = valor;
}

function setHandlers(cast) {
  var volumeSlider = document.getElementById(`volume-${cast}`);
  var positionSlider = document.getElementById(`position-${cast}`);
  //var slidertitle = document.getElementById(`positiontitle-${cast}`);
  var back = document.getElementById(`back-${cast}`);
  var back10 = document.getElementById(`back10-${cast}`);
  var play = document.getElementById(`play-${cast}`);
  var pause = document.getElementById(`pause-${cast}`);
  var forward10 = document.getElementById(`forward10-${cast}`);
  var forward = document.getElementById(`forward-${cast}`);
  var mute = document.getElementById(`mute-${cast}`);
  var unmute = document.getElementById(`unmute-${cast}`);

  positionSlider.oninput = function () {
    this.style.background = `linear-gradient(to right, rgb(var(--acento)) ${this.value}%, rgb(var(--lineas)) ${this.value}%)`;
  };

  positionSlider.onmouseup = function () {
    f_position(cast, this.value);
  };

  positionSlider.ontouchend = function () {
    f_position(cast, this.value);
  };

  positionSlider.onmousemove = function (event) {
    var parent = document.getElementById(`image-${cast}`);
    var totalDuration = document
      .getElementById(`position-${cast}`)
      .getAttribute("duration");
    var slidertitle = document.getElementById(`positiontitle-${cast}`);
    var sliderOffsetX =
      positionSlider.getBoundingClientRect().left -
      document.documentElement.getBoundingClientRect().left;
    var sliderOffsetY =
      positionSlider.getBoundingClientRect().top -
      document.documentElement.getBoundingClientRect().top;
    var sliderWidth = positionSlider.offsetWidth - 1;
    var currentMouseXPos = event.clientX + window.pageXOffset - sliderOffsetX;

    newPosX = 0;
    titleWidth = slidertitle.offsetWidth;
    if (currentMouseXPos + titleWidth / 2 > parent.offsetWidth - 6) {
      newPosX = parent.offsetWidth - titleWidth - 6;
    } else {
      if (currentMouseXPos - 2 < titleWidth / 2) {
        newPosX = 2;
      } else {
        newPosX = currentMouseXPos - titleWidth / 2;
      }
    }
    slidertitle.style.top = sliderOffsetY - 15 + "px";
    slidertitle.style.left = newPosX + "px";

    currentPosition = totalDuration * (currentMouseXPos / sliderWidth);
    if (currentPosition < 0) {
      currentPosition = 0;
    }
    if (currentPosition > totalDuration) {
      currentPosition = totalDuration;
    }

    var positionSeconds = Math.floor(currentPosition % 60);
    var positionMinutes = Math.floor(currentPosition / 60) % 60;
    var positionHours = Math.floor(currentPosition / (60 * 60));
    var totalHours = Math.floor(totalDuration / (60 * 60));

    if (totalHours > 0) {
      format = "HH:MM:SS";
    } else {
      format = "MM:SS";
    }

    texto = format.replace("HH", ("100000" + positionHours).slice(-2));
    texto = texto.replace("MM", ("100000" + positionMinutes).slice(-2));
    texto = texto.replace("SS", ("100000" + positionSeconds).slice(-2));

    slidertitle.innerHTML = texto;
    slidertitle.style.display = "block";
  };

  positionSlider.onmouseleave = function () {
    var slidertitle = document.getElementById(`positiontitle-${cast}`);
    slidertitle.style.display = "none";
  };

  volumeSlider.oninput = function () {
    this.style.background = `linear-gradient(to right, rgb(var(--acento)) ${this.value}%, rgb(var(--lineas)) ${this.value}%)`;
  };

  volumeSlider.onmouseup = function () {
    f_volumen(cast, this.value);
  };

  volumeSlider.ontouchend = function () {
    f_volumen(cast, this.value);
  };

  back.onclick = function () {
    f_back(cast);
  };

  back10.onclick = function () {
    f_back10(cast);
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

  forward10.onclick = function () {
    f_forward10(cast);
  };

  forward.onclick = function () {
    f_forward(cast);
  };

  mute.onclick = function () {
    f_mute(cast);

    var mute = document.getElementById(`mute-${cast}`);
    var unmute = document.getElementById(`unmute-${cast}`);
    mute.style.display = "none";
    unmute.style.display = "inherit";
  };

  unmute.onclick = function () {
    f_unmute(cast);

    var mute = document.getElementById(`mute-${cast}`);
    var unmute = document.getElementById(`unmute-${cast}`);
    unmute.style.display = "none";
    mute.style.display = "inherit";
  };
}

function atender(message) {
  jsonObject = JSON.parse(message.data);
  var resultado = atender_recursivo(jsonObject, "");
  var aux = resultado.split(",");
  if (aux[0] == "REMOVE") removeCard(aux[1]);
}

function atender_recursivo(jsonObject, cast) {
  var local_cast = cast;
  var retorno = "";
  for (var key in jsonObject) {
    if (key == "cast") {
      local_cast = jsonObject[key];
      createCard(local_cast);
    }
    if (jsonObject[key] instanceof Object) {
      retorno = atender_recursivo(jsonObject[key], local_cast);
    } else {
      retorno = atender_final(key, jsonObject[key], local_cast);
    }
  }
  return retorno;
}

function atender_final(key, value, cast) {
  var retorno = "";
  switch (key) {
    case "position":
      setPosition(cast, parseFloat(value) * 100);
      break;
    case "duration":
      setDuration(cast, parseFloat(value));
      break;
    case "volume":
      setVolume(cast, parseFloat(value) * 100);
      break;
    case "title":
      setTitle(cast, value);
      break;
    case "subtitle":
      setSubTitle(cast, value);
      break;
    case "series":
      setSeries(cast, value);
      break;
    case "season":
      setSeason(cast, value);
      break;
    case "episode":
      setEpisode(cast, value);
      break;
    case "state":
      retorno = `${value},${cast}`;
      setState(cast, value);
      break;
    case "image":
      setImage(cast, value);
      break;
    case "artist":
      setArtist(cast, value);
      break;
    case "album":
      setAlbum(cast, value);
      break;
  }
  return retorno;
}

function removeCard(cast) {
  var card = document.getElementById(cast);
  if (card) card.parentNode.removeChild(card);
}

function createCard(cast) {
  newDiv = document.getElementById(cast);
  grid = document.getElementById("grid");
  if (!newDiv) {
    card = document.createElement("div");
    card.setAttribute(
      "class",
      "mdl-card mdl-cell mdl-cell--6-col mdl-cell--4-col-tablet mdl-shadow--2dp"
    );
    card.setAttribute("id", cast);

    header = document.createElement("div");
    header.setAttribute("class", "cast");
    header.setAttribute("id", `cast-${cast}`);
    header.innerHTML = cast;
    card.appendChild(header);

    image = document.createElement("div");
    image.setAttribute("class", "mdl-card__media");
    image.setAttribute("id", `image-${cast}`);
    image.setAttribute("style", "background: url('images/black.png') 50% 50%");

    posSlider = document.createElement("input");
    posSlider.setAttribute("class", "slider");
    posSlider.setAttribute("type", "range");
    posSlider.setAttribute("min", "0");
    posSlider.setAttribute("max", "100");
    posSlider.setAttribute("id", `position-${cast}`);
    image.appendChild(posSlider);
    posTitle = document.createElement("div");
    posTitle.setAttribute("class", "slider-title");
    posTitle.setAttribute("id", `positiontitle-${cast}`);
    image.appendChild(posTitle);
    card.appendChild(image);

    support = document.createElement("div");
    support.setAttribute("class", "mdl-card__supporting-text");
    support.setAttribute("id", `text-${cast}`);

    volume = document.createElement("div");
    volume.setAttribute("class", "volume");

    mute = document.createElement("i");
    mute.setAttribute("class", "fas fa-volume-up");
    mute.setAttribute("id", `mute-${cast}`);
    volume.appendChild(mute);

    unmute = document.createElement("i");
    unmute.setAttribute("class", "fas fa-volume-mute");
    unmute.setAttribute("id", `unmute-${cast}`);
    volume.appendChild(unmute);

    volumeSlider = document.createElement("input");
    volumeSlider.setAttribute("class", "slider");
    volumeSlider.setAttribute("type", "range");
    volumeSlider.setAttribute("min", "0");
    volumeSlider.setAttribute("max", "100");
    volumeSlider.setAttribute("id", `volume-${cast}`);
    volume.appendChild(volumeSlider);

    support.appendChild(volume);

    content = document.createElement("div");
    content.setAttribute("class", "content");
    content.setAttribute("id", `content-${cast}`);

    title = document.createElement("div");
    title.setAttribute("class", "title");
    title.setAttribute("id", `title-${cast}`);

    content.appendChild(title);

    subtitle = document.createElement("div");
    subtitle.setAttribute("class", "subtitle");
    subtitle.setAttribute("id", `subtitle-${cast}`);

    content.appendChild(subtitle);

    support.appendChild(content);

    controls = document.createElement("div");
    controls.setAttribute("class", "controls");
    controls.setAttribute("id", `controls-${cast}`);

    back = document.createElement("i");
    back.setAttribute("class", "fas fa-step-backward");
    back.setAttribute("id", `back-${cast}`);
    controls.appendChild(back);

    back10 = document.createElement("i");
    back10.setAttribute("class", "fas fa-undo");
    back10.setAttribute("id", `back10-${cast}`);
    controls.appendChild(back10);

    play = document.createElement("i");
    play.setAttribute("class", "fas fa-play-circle fa-3x");
    play.setAttribute("id", `play-${cast}`);
    controls.appendChild(play);

    pause = document.createElement("i");
    pause.setAttribute("class", "fas fa-pause-circle fa-3x");
    pause.setAttribute("id", `pause-${cast}`);
    controls.appendChild(pause);

    forward10 = document.createElement("i");
    forward10.setAttribute("class", "fas fa-redo");
    forward10.setAttribute("id", `forward10-${cast}`);
    controls.appendChild(forward10);

    forward = document.createElement("i");
    forward.setAttribute("class", "fas fa-step-forward");
    forward.setAttribute("id", `forward-${cast}`);
    controls.appendChild(forward);

    support.appendChild(controls);

    card.appendChild(support);

    grid.appendChild(card);

    setHandlers(cast);
  }
}

function randomgb() {
  number = Math.floor(Math.random() * 449 + 1).pad(3);
  image = "/images/image_" + number + ".jpg";

  var img = document.createElement("img");
  img.setAttribute("src", image);

  img.addEventListener("load", function () {
    var vibrant = new Vibrant(img);
    var swatches = vibrant.swatches();
    for (var swatch in swatches)
      if (swatches.hasOwnProperty(swatch) && swatches[swatch]) {
        var rgb = swatches[swatch].getRgb();
        var variable =
          Math.floor(rgb[0]) +
          "," +
          Math.floor(rgb[1]) +
          "," +
          Math.floor(rgb[2]);
        if (swatch == "Vibrant") {
          document.documentElement.style.setProperty("--acento", variable);
        }
        if (swatch == "DarkVibrant") {
          //document.documentElement.style.setProperty('--texto-principal', variable);
          //document.documentElement.style.setProperty('--texto-secundario', variable);
        }
        if (swatch == "LightVibrant") {
          //No hago nada
        }
        if (swatch == "Muted") {
          document.documentElement.style.setProperty("--fondo", variable);
        }
        if (swatch == "DarkMuted") {
          document.documentElement.style.setProperty("--lineas", variable);
        }
      }
  });
  document.body.style.background = "url('" + image + "')";
}

window.onload = function () {
  var full =
    window.location.hostname +
    (window.location.port ? ":" + window.location.port : "");
  ws = new WebSocket("ws://" + full + "/websocket");

  ws.onopen = function () {
    Console.log("WebSocket abierto");
    ws.send("init");
    actualizar = setInterval(function() {ws.send("update")}, 1000);
  };

  ws.onmessage = function (evt) {
    atender(evt);
  };

  ws.onclose = function () {
    Console.log("WebSocket cerrado");
    while (actualizar) {
      window.clearInterval(actualizar);
    }
  };

  document.body.ondblclick = function () {
    randomgb();
  };
  randomgb();
};
