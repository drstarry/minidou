%scripts=get('scripts', [])
%scripts[:0] = ["/static/js/jquery-2.0.1.min.js",
%       "/static/bootstrap/js/bootstrap.min.js",
%       "/static/js/jquery.js",
%       "/static/js/d3.v3.min.js"]
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MiniDou</title>

  <link rel="stylesheet" type="text/css" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css" media="all" />
  <link rel="stylesheet" type="text/css" href="/static/bootstrap/css/bootstrap-responsive.css" media="all" />
  <link href="//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css" rel="stylesheet">
  <link
        rel="stylesheet"
        href="http://cdn.leafletjs.com/leaflet-0.7/leaflet.css"
    />

  %for script in scripts:
  <script src="{{script}}"></script>
  %end
  <script
        src="http://cdn.leafletjs.com/leaflet-0.7/leaflet.js">
    </script>
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
        <a class="navbar-brand" href="/minidou">MiniDou</a>
      </div>
	<div class="navbar-collapse collapse">
        <ul class="nav navbar-nav">
          <li class="dropdown">
            <a href="/crawl" class="dropdown-toggle" data-toggle="dropdown">
              Crawler|爬虫 <b class="caret"></b>
            </a>
            <ul class="dropdown-menu">
              <li>
                <a href="/event">Douban location|同城</a>
              </li>
              <li>
                <a href="/movie">Douban movie|电影</a>
              </li>
            </ul>
          </li>
          <li class="dropdown">
            <a href="/crawl" class="dropdown-toggle" data-toggle="dropdown">
              Visualization|可视化
              <b class="caret"></b>
            </a>
            <ul class="dropdown-menu">
              <li>
                <a href="/vis_events">Events Map|活动分布</a>
              </li>
              <li>
                <a href="/vis_actor">Co-actor network|合作出演</a>
              </li>
              <li>
                <a href="/vis_review">Hot words|影评关键词 </a>
              </li>
            </ul>
          </li>
        </ul>
        <ul class="nav navbar-nav navbar-right">

          <li>
            <a href="/about">About</a>
          </li>
        </ul>
      </div>
      <!--/.nav-collapse --> </div>
  </div>
</br>
</br>
<div class="container" >
  %include
</div>
<!-- FOOTER -->

</body>

</html>
