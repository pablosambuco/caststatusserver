<!DOCTYPE html>
<html>

<head>
    <title>Cast Status</title>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="Cast Status" />
    <meta name="author" content="Pablo Sambuco" />
    <link rel="icon" type="image/png" href="/images/favicon.png" />
    <link rel="stylesheet" type="text/css" href="/static/login.css" />
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vibrant.js/1.0.0/Vibrant.js"></script>
    <script src="static/main.js"></script>
</head>

<body>
    <div id="container">
        <section class="ftco-section">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-md-6 text-center mb-5">
                        <h2 class="heading-section">CastStatusServer</h2>
                    </div>
                </div>
                <div class="row justify-content-center">
                    <div class="col-md-6 col-lg-4">
                        <div class="login-wrap p-0">
                            <h3 class="mb-4 text-center">Login</h3>
                            <form action="/" method="post" class="signin-form">
                                <div class="form-group">
                                    <input name="username" class="form-control" placeholder="user" type="text" autocomplete="username"/>
                                </div>
                                <div class="form-group">
                                    <input name="password" class="form-control" placeholder="pass" type="password" autocomplete="current-password" />
                                </div>
                                <div class="form-group">
                                    <input value="Login" class="form-control" type="submit" />
                                </div>
                                <input name="fn" type="hidden" value="{{filename}}" />
                            </form>
                            <p class="rojo w-100 text-center">{{error}}</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</body>

</html>