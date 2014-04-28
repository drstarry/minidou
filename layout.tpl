%scripts=get('scripts', [])
%scripts[:0] = ["/static/jquery-2.0.1.min.js",
%				"/static/bootstrap/js/bootstrap.min.js",
%				"/static/d3.v3.min.js"]

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
</head>
<body>


     <div class="collapse navbar-collapse " id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li class="">
          <a href="/" ><h4>Social Crawl</h4></a>
        </li>
        <li class="active">
          <a href="/enron/network/"><h4>Weibo</h4></a>
        </li>
        <li class="active">
          <a href="/enron/topic/"><h4>Flickr</h4></a>
        </li>
        <li class="active">
          <a href="/enron/topic/"><h4>Myspace</h4></a>
        </li>
         <li class="active">
          <a href="/about"><h4>About</h4></a>
        </li>
      </ul>
    </div>
    <div class="container">
        %include
    </div>

</body>
</html>
