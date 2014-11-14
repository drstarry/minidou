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
      <h4>Movie you want to get <b>id</b>,</h4>
      <h4>
        and the params of co-actor network  <b>degree</b>
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
            爬虫参数设置：
          </legend>
        </div>

        <div class="control-group">

          <!-- Text input-->

          <h3>
            <span class="label label-info">待爬取电影ID</span>

            <input name="id" type="text" placeholder="id" class="input-xlarge">
            <span class="label label-warning">eg.6082518(超凡蜘蛛侠2)</span>
          </h3>
          <p class="help-block">注意:id不是用户名，用户名可以有重复，而id是每个用户的唯一凭证哦</p>
        </div>

        <div class="control-group">

          <!-- Select Basic -->
          <h3>
            <span class="label label-info">演员合作关系深度的深度</span>

            <input name="degree" type="text" placeholder="degree" class="input-xlarge"></h3>
          <p class="help-block">提示:我们把和该用户直接相连的邻居节点度数设为1，依此类推</p>
        </div>

        <div class="control-group">

          <!-- Select Basic -->
          <h3>
            <span class="label label-info">影评个数</span>

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
            <input type="submit" class="btn btn-success" value="开始"></div>
        </div>
      </div>
    </fieldset>
  </form>
</div>

</div>

<div id="pop" style="position:absolute; display:none; left:-1px; top:1px; width:100%; height:100%; background-color:white; z-index:1000; text-align:center;margin:0px auto; opacity:0.3">
<table border="0" style=" margin: auto;">
<tr><td ><span id="disp" ><h2>小豆正在努力爬！请稍等！</h2></span></td></tr>
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
