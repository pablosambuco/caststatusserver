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
    console.log(cast,"forward");
  };
}

  // key_lookup = {
  //   'volume_level': 'volume',
  //   'title': 'title',
  //   'subtitle': 'subtitle',
  //   'series_title': 'series',
  //   'season': 'season',
  //   'episode': 'episode',
  //   'artist': 'artist',
  //   'album_name': 'album',
  //   'track': 'track',
  //   'images': 'image',
  //   'player_state': 'state',
  //   'volume_muted': 'mute',
  //   'status_text': 'text',
  //   'icon_url': 'icon'
  // }

function atender(message) {
  var msg = "";
  var name = "";
  var jsonObject = "";
  try {
    jsonObject = JSON.parse(message.data);
    console.log(`${jsonObject}`);
    name = jsonObject.name;
    //console.log(`${name}`);
    msg = jsonObject.message;
    //console.log(`${msg}`);
  } 
  catch(err){
      //NADA
  }
  //console.log(`${message.data}`);
  //TODO tratar los mensajes
}