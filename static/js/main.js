require.config({
        paths: { vibrant: 'https://cdnjs.cloudflare.com/ajax/libs/vibrant.js/1.0.0/Vibrant' }
    });

require(['vibrant'], function(vib) { 
    function Vibrant(img, count, quali) {
       return vib.Vibrant(img, count, quali)
    }
  });

var ws = "";
var timer = "";

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

function f_forward(cast) {
  ws.send(`forward,${cast}`);
}

function f_volumen(cast, valor) {
  ws.send(`volume,${cast},${valor}`);
}

function setVolume(cast, valor) {
  var element = document.getElementById(`volume-${cast}`);
  element.value = valor;
  element.style.background = `linear-gradient(to right, rgb(var(--acento)) ${element.value}%, rgb(var(--lineas)) ${element.value}%)`;
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
  if (element) element.style = `background: url(${valor}) 50% 50%; background-size: 450px;`;
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
  var slider = document.getElementById(`volume-${cast}`);
  var back = document.getElementById(`back-${cast}`);
  var play = document.getElementById(`play-${cast}`);
  var pause = document.getElementById(`pause-${cast}`);
  var forward = document.getElementById(`forward-${cast}`);

  slider.oninput = function () {
    this.style.background = `linear-gradient(to right, rgb(var(--acento)) ${this.value}%, rgb(var(--lineas)) ${this.value}%)`;
  };

  slider.onmouseup = function () {
    f_volumen(cast, this.value);
  };

  slider.ontouchend = function () {
    f_volumen(cast, this.value);
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
      switch (key) {
        case "volume":
          setVolume(local_cast, parseFloat(jsonObject[key]) * 100);
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
          retorno = `${jsonObject[key]},${local_cast}`;
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
    card.appendChild(image);

    support = document.createElement("div");
    support.setAttribute("class", "mdl-card__supporting-text");
    support.setAttribute("id", `text-${cast}`);

    volume = document.createElement("div");
    volume.setAttribute("class", "volume");

    volumeDown = document.createElement("i");
    volumeDown.setAttribute("class", "fas fa-volume-down");
    volume.appendChild(volumeDown);

    volumeSlider = document.createElement("input");
    volumeSlider.setAttribute("class", "slider");
    volumeSlider.setAttribute("type", "range");
    volumeSlider.setAttribute("min", "1");
    volumeSlider.setAttribute("max", "100");
    volumeSlider.setAttribute("id", `volume-${cast}`);
    volume.appendChild(volumeSlider);

    volumeUp = document.createElement("i");
    volumeUp.setAttribute("class", "fas fa-volume-up");
    volume.appendChild(volumeUp);

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

    play = document.createElement("i");
    play.setAttribute("class", "fas fa-play-circle fa-3x");
    play.setAttribute("id", `play-${cast}`);
    controls.appendChild(play);

    pause = document.createElement("i");
    pause.setAttribute("class", "fas fa-pause-circle fa-3x");
    pause.setAttribute("id", `pause-${cast}`);
    controls.appendChild(pause);

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
      if (swatches.hasOwnProperty(swatch) && swatches[swatch])
      {
        var rgb = swatches[swatch].getRgb()
        var variable = Math.floor(rgb[0])+","+Math.floor(rgb[1])+","+Math.floor(rgb[2])
        if (swatch == "Vibrant") {
          document.documentElement.style.setProperty('--acento', variable);
          
        }
        if (swatch == "DarkVibrant"){
          //document.documentElement.style.setProperty('--texto-principal', variable);
          //document.documentElement.style.setProperty('--texto-secundario', variable);          
          
        }
        if (swatch == "LightVibrant"){
          
        }
        if (swatch == "Muted"){
          document.documentElement.style.setProperty('--fondo', variable);
          
        }
        if (swatch == "DarkMuted"){
          document.documentElement.style.setProperty('--lineas', variable);
          
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
    console.log("WebSocket abierto");
    ws.send("init");
  };

  ws.onmessage = function (evt) {
    atender(evt);
  };

  ws.onclose = function () {
    console.log("WebSocket cerrado");
    while (timer) {
      window.clearInterval(timer--);
    }
  };

  document.body.ondblclick = function () {
    randomgb();
  };
  randomgb();
};
