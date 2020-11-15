<!DOCTYPE html>
<html>

<head>
    <title>Cast Status</title>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Cast Status">
    <meta name="author" content="Pablo Sambuco">
    <link rel="icon" type="image/png" href="/images/favicon.png">
    <link rel="stylesheet" type="text/css" href="/static/estilo.css">
    <script type="text/javascript" src="/static/funciones.js" )"></script>
    <script src="https://kit.fontawesome.com/cea894e75c.js" crossorigin="anonymous"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>

    <script type="text/javascript">
        var ws = new WebSocket("ws://" + window.location.hostname + ":8083/websocket");
        function init() {
            var timer = "";
            
            ws.onopen = function () {
                console.log("WebSocket abierto");
                ws.send("init");
                timer = setInterval(actualizar, 1000);            
            };
            ws.onmessage = function (evt) {
                console.log(evt);
            };
            ws.onclose = function () {
                console.log("WebSocket cerrado");
                clearInterval(timer);
            };
        };
        
        function actualizar() {
            ws.send("update");
        };
    
        window.onload = function() {
            % for cast in data:
                setVolume("{{cast}}",50);    
            % end
            % for cast in data:
                setHandlers("{{cast}}");
            % end
            init();
        }
    </script>
</head>

<body>
    <div id="coso"></div>
    <div class="mdl-layout mdl-js-layout mdl-color--grey-100">
        <main class="mdl-layout__content">
            <div class="mdl-grid">
                % for cast in data:
                <div class="mdl-card mdl-cell mdl-cell--6-col mdl-cell--4-col-tablet mdl-shadow--2dp" id="{{cast}}">
                    <div class="cast" id="titulo-{{cast}}" data-uuid="">{{cast}}</div>
                    <div class="mdl-card__media" id="imagen-{{cast}}" style="background: url('images/black.png') 50% 50%"></div>
                    <div class="mdl-card__supporting-text" id="support-{{cast}}">
                        <div class="volumen">
                            <i class="fas fa-volume-down"></i>
                            <input type="range" min="1" max="100" class="slider" id="volume-{{cast}}" />
                            <i class="fas fa-volume-up"></i>
                        </div>
                        <div class="contenido" id="contenido-{{cast}}">
                            <div class="titulo" id="titulo-{{cast}}"></div>
                            <div class="subtitulo" id="subtitulo-{{cast}}"></div>
                        </div>
                        <div class="controles" id="controles-{{cast}}">
                            <i class="fas fa-step-backward" id="back-{{cast}}"></i>
                            <i class="fas fa-play-circle fa-3x" id="play-{{cast}}"></i>
                            <i class="fas fa-pause-circle fa-3x" id="pause-{{cast}}"></i>
                            <i class="fas fa-step-forward" id="forward-{{cast}}"></i>
                        </div>
                    </div>
                </div>
                % end
            </div>
        </main>
    </div>
</body>

</html>