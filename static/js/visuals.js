Number.prototype.pad = function (size) {
  var s = String(this);
  while (s.length < (size || 2)) {
    s = "0" + s;
  }
  return s;
};

function randomgb() {
  var number = Math.floor(Math.random() * 449 + 1).pad(3);
  var image = "/images/image_" + number + ".jpg";

  var img = document.createElement("img");
  img.setAttribute("src", image);

  img.addEventListener("load", function () {
    var vibrant = new Vibrant(img);
    var swatches = vibrant.swatches();
    for (var swatch in swatches) {
      if (swatches.hasOwnProperty(swatch) && swatches[swatch]) {
        var rgb = swatches[swatch].getRgb();
        var variable =
          Math.floor(rgb[0]) +
          "," +
          Math.floor(rgb[1]) +
          "," +
          Math.floor(rgb[2]);
        if (swatch === "Vibrant") {
          document.documentElement.style.setProperty("--acento", variable);
        }
        if (swatch === "DarkVibrant") {
          //document.documentElement.style.setProperty('--texto-principal', variable);
          //document.documentElement.style.setProperty('--texto-secundario', variable);
        }
        if (swatch === "LightVibrant") {
          //No hago nada
        }
        if (swatch === "Muted") {
          document.documentElement.style.setProperty("--fondo", variable);
        }
        if (swatch === "DarkMuted") {
          document.documentElement.style.setProperty("--lineas", variable);
        }
      }
    }
  });
  document.body.style.background = "url('" + image + "')";
}

window.onload = function () {
  document.body.ondblclick = function () {
    randomgb();
  };
  randomgb();
};
