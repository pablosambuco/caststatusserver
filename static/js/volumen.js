$("#volume").slider({
  	min: 0,
  	max: 100,
  	value: 0,
   range: "min",
  	slide: function(event, ui) {
    	setVolume(ui.value / 100);
  	}
});
	
var myMedia = document.createElement('audio');
$('#player').append(myMedia);
myMedia.id = "myMedia";

playAudio('http://emilcarlsson.se/assets/Avicii%20-%20The%20Nights.mp3', 0);

function playAudio(fileName, myVolume) {
   myMedia.src = fileName;
   myMedia.setAttribute('loop', 'loop');
   setVolume(myVolume);
   myMedia.play();
}

function setVolume(myVolume) {
   var myMedia = document.getElementById('myMedia');
   myMedia.volume = myVolume;
}

document.getElementById("volume") = function() {
  this.style.background = 'linear-gradient(to right, #82CFD0 0%, #82CFD0 ' + this.value + '%, #fff ' + this.value + '%, white 100%)'
};