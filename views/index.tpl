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
    <!--script type="text/javascript" src="/static/jquery.min.js"></script-->
    <!--script type="text/javascript" src="/static/bootstrap.min.js"></script--> 
</head>
<body>
    <!--
    <img src="/images/base.png" class="base" />
    <img src="/images/play.png" class="boton" />
    <img src="https://i.ytimg.com/vi/k0Q8CUhTlxw/hqdefault.jpg" class="imagen">
    -->
    <div class="container">
    % for cast in data:
         {{cast}}
         % for att in data[cast]:
            {{att}}: {{data[cast][att]}}
         % end
    % end
    </div> 
    <!-- /container -->
</body>
</html>
