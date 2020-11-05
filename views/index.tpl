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
    <script type="text/javascript" src="/static/volumen.js"></script>
    
</head>
<body>
    <!--
    <img src="/images/base.png" class="base" />
    <img src="/images/play.png" class="boton" />
    <img src="https://i.ytimg.com/vi/k0Q8CUhTlxw/hqdefault.jpg" class="imagen">
    -->
<div class="mdl-layout mdl-js-layout mdl-color--grey-100">
    <main class="mdl-layout__content">
        <div class="mdl-grid">
            % for cast in data:
            <div class="mdl-card mdl-cell mdl-cell--6-col mdl-cell--4-col-tablet mdl-shadow--2dp">
               % for att in data[cast]:
                  % if(att == "imagen"):             
                     <a href="#">
                     <div class="mdl-card__media" style="background: url({{data[cast][att]}}) 50% 50%">
                     
                     </div>
                     </a>
                  % elif(att == "cast"):
                     <div class="mdl-card__title">
                        <h1 class="mdl-card__title-text">{{cast}}</h1>
                     </div>
                  % end
               % end
               <div class="mdl-card__supporting-text">
               % for att in data[cast]:
                  % if(att == "volumen"): 
                  <div id="player">
                     <i class="fa fa-volume-down"></i>
                     <div id="volume"></div>
                     <i class="fa fa-volume-up"></i>
                     <script>
                         setVolume({{"{:.0f}".format(100*float(data[cast][att]))}});
                     </script>                     
                  </div>                  
                   % end
               %end
               % for att in data[cast]:
                  % if(att == "titulo"):             
                     <span class="titulo">{{data[cast][att]}}</span><br />
                  % end
               %end
               % for att in data[cast]:
                  % if(att == "artista"):             
                     <span class="artista">{{data[cast][att]}}</span>
                  % end
               %end
               </div>                
            </div> 
            % end
        </div>
    </main>
</div>
    
</body>
</html>
