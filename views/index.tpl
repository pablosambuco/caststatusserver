<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Bottle web project template">
    <meta name="author" content="datamate">
    <link rel="icon" type="image/png" href="/images/favicon.png">
    <title>Project</title>
    <link rel="stylesheet" type="text/css" href="/static/estilo.css">
    <script type="text/javascript" src="/static/funciones.js" )"></script>
    <script src="https://kit.fontawesome.com/cea894e75c.js" crossorigin="anonymous"></script>
</head>

<body>
    <div class="mdl-layout mdl-js-layout mdl-color--grey-100">
        <main class="mdl-layout__content">
            <div class="mdl-grid">
                % for cast in data:
                <div class="mdl-card mdl-cell mdl-cell--6-col mdl-cell--4-col-tablet mdl-shadow--2dp">
                    <div class="cast" id="{{cast}}" data-uuid="{{data[cast]["uuid"]}}">{{cast}}</div>
                    % for att in data[cast]:
                    % if(att == "imagen"):
                      <div class="mdl-card__media" style="background: url({{data[cast][att]}}) 50% 50%"></div>
                    % elif(att == "cast"):
                    <div class="mdl-card__title">
                        <h1 class="mdl-card__title-text">{{cast}}</h1>
                    </div>
                    % end
                    % end
                    <div class="mdl-card__supporting-text">
                        % for att in data[cast]:
                        % if(att == "volumen"):
                        <div class="volumen">
                            <i class="fas fa-volume-down"></i>
                            <input type="range" min="1" max="100" class="slider" id="volume-{{cast}}" />
                            <i class="fas fa-volume-up"></i>
                        </div>
                        % end
                        %end
                        <div class="contenido">
                            % for att in data[cast]:
                            % if(att == "titulo"):
                            <div class="titulo">{{data[cast][att]}}</div>
                            % end
                            %end
                            % for att in data[cast]:
                            % if(att == "artista"):
                            <div class="subtitulo">{{data[cast][att]}}</div>
                            % end
                            %end
                        </div>
                        <div class="controles">
                            % for att in data[cast]:
                            % if(att == "volumen"):
                            <i class="fas fa-step-backward" id="back-{{cast}}"></i>
                            <i class="fas fa-play-circle fa-3x" id="play-{{cast}}"></i>
                            <i class="fas fa-pause-circle fa-3x" id="pause-{{cast}}"></i>
                            <i class="fas fa-step-forward" id="forward-{{cast}}"></i>
                            % end
                            %end
                        </div>
                    </div>
                </div>
                % end
                <script>
                  window.onload = function() {
                     % for cast in data:
                     % for att in data[cast]:
                     % if (att == "volumen"):
                        setVolume("{{cast}}",{{"{:.0f}".format(100*float(data[cast][att]))}});
                        setHandlers("{{cast}}","{{data[cast]["uuid"]}}");
                     % end 
                     % end 
                     % end
                  }
                </script>
            </div>
        </main>
    </div>

</body>

</html>