%scripts=get('scripts', [])
%scripts[:0] = ["/static/jquery-2.0.1.min.js",
%				"/static/bootstrap/js/bootstrap.min.js",
%				"/static/d3.v3.min.js"]

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
    <link rel="stylesheet" type="text/css" href="/static/bootstrap/css/bootstrap.css" media="all" />
    <link rel="stylesheet" type="text/css" href="/static/bootstrap/css/bootstrap-responsive.css" media="all" />
    %for script in scripts:
    <script src="{{script}}"></script>
    %end
</head>
<body>
    <div class="navbar">
        <div class="navbar-inner">
            <a class="brand" href="/">Social Crawl+Visualisation</a>
            <ul class="nav">
                <li> <a href="/academic/search">Weibo</a> </li>
                <li> <a href="/patent/search">Flickr</a> </li>
                <li> <a href="/weibo/search">Myspace</a> </li>
		<li> <a href="/about">About</a> </li>
            </ul>
        </div>
    </div>
    <div class="container">
        %include
    </div>

</body>
</html>
