<style type="text/css">
  form.form-inline {
    display: inline-block;
  }
</style>

<div class="row">
  <div class="col-md-5">
    <div class="panel panel-default">
      <div class="panel-heading">
      <h2> <img src="http://img3.douban.com/favicon.ico"></img>Douban movie</h2>
    </div>
    <div class="panel-body">
      <h4>Input <b>id</b> of the movie you want,</h4>
      <h4>
        the <b>degree</b> of co-actor network,  
        and the <b>number</b> of movie review
      </h4>
      <h4>
        Click
        <b>START!</b>
      </h4>

    </div>
  </div>
</div>

<div class="col-md-7">

  <div class="extra-results">
    <form class="form-horizontal" onSubmit="winload()" enctype="multipart/form-data" method="post" action="/crawl/movie">
      <fieldset>
        <div id="legend" class="">
          <legend> <i class="fa fa-gear fa-2x pull-left"></i>
            Parameters：
          </legend>
        </div>

        <div class="control-group">

          <!-- Text input-->

          <h3>
            <span class="label label-info">movie ID</span>

            <input name="id" type="text" placeholder="id" class="input-xlarge">
            <span class="label label-warning">eg.1889243(Interstellar)</span>
          </h3>
          <p class="help-block">ps: ID is the identification of a movie</p>
        </div>

        <div class="control-group">

          <!-- Select Basic -->
          <h3>
            <span class="label label-info">degree of co-actor network</span>

            <input name="degree" type="text" placeholder="degree" class="input-xlarge"></h3>
          <p class="help-block">ps: Direct connection mean degree one</p>
        </div>

        <div class="control-group">

          <!-- Select Basic -->
          <h3>
            <span class="label label-info">number of movie review</span>

            <select name="rtype" class="form-control xlarge" >
              <option>1.5</option>
              <option>2.10</option>
              <option>2.20</option>
            </select>
          </h3>
          <p class="help-block"></p>
        </div>


        <div class="control-group">
          <label class="control-label"></label>

          <!-- Button -->
          <div class="controls">
            <input type="submit" class="btn btn-success" value="Start!"></div>
        </div>
      </div>
    </fieldset>
  </form>
</div>

</div>

<div id="pop" style="position:absolute; display:none; left:-1px; top:1px; width:100%; height:100%; background-color:white; z-index:1000; text-align:center;margin:0px auto; opacity:0.3">
<table border="0" style=" margin: auto;">
<tr><td ><span id="disp" ><h2>I'm crawling! Hold on! </h2></span></td></tr>
<tr><td style="text-align:center"><img src="/static/img/loading.gif"></td></tr>
</table>
</div>


<script>
 function winload(){

     document.getElementById("pop").style.display="block";
     //f8=true;
}
</script>

%rebase layout
