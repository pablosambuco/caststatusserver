var ws = "";
var timer = "";

window.onload = function() {
    var full = window.location.hostname+(window.location.port ? ':' + window.location.port:'');
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
        while(timer) {
            window.clearInterval(timer--);
        };
    };
                
};