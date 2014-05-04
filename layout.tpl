%scripts=get('scripts', [])
%scripts[:0] = ["/static/js/jquery-2.0.1.min.js",
%				"/static/bootstrap/js/bootstrap.min.js",
%				"/static/js/d3.v3.min.js"]

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Social</title>
    <link rel="shortcut icon" type="image/x-icon"  media="screen">
    <link rel="stylesheet" type="text/css" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css" media="all" />
    <link rel="stylesheet" type="text/css" href="/static/bootstrap/css/bootstrap-responsive.css" media="all" />
    <link href="//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css" rel="stylesheet">

    %for script in scripts:
    <script src="{{script}}"></script>
    %end

    <style type="text/css">

        .container {

          height: 100%;

        }


    </style>
</head>
<body style="height: 100%">

<div class="navbar navbar-default navbar-static-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/">Social Mini</a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="/weibo">Weibo</a></li>
            <li><a href="/analysis/none">Analysis</a></li>
            <li><a href="/vis/none">Visualization</a></li>


          </ul>
          <ul class="nav navbar-nav navbar-right">
            <li><a href="/help">Help</a></li>
            <li><a href="/about">About</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </div>
    </br>
    </br>
    <div class="container" >
        %include
    </div>
<!-- FOOTER -->



</body>


</html>
