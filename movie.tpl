<style type="text/css">
  form.form-inline {
    display: inline-block;
  }
</style>

<div class="row">
  <div class="col-md-5">
    <div class="panel panel-default">
      <div class="panel-heading">
      <h2> <img src="http://img3.douban.com/favicon.ico"></img>豆瓣电影数据抓取</h2>
    </div>
    <div class="panel-body">
      <h4>请输入您想要抓取的电影<b>id</b>,</h4>
      <h4>
        并选取想要抓取 <b>演员合作关系深度</b>
        和该电影的 <b>影评类型</b>
      </h4>
      <h4>
        点击
        <b>开始</b>
        进行抓取
      </h4>

    </div>
  </div>
</div>

<div class="col-md-7">

  <div class="extra-results">
    <form class="form-horizontal" enctype="multipart/form-data" method="post" action="/crawl/movie">
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
            <span class="label label-info">影评类型</span>

            <select name="rtype" class="form-control xlarge" >
              <option>1.热门影评</option>
              <option>2.最新影评</option>
            </select>
          </h3>
          <p class="help-block"></p>
        </div>

        <!-- <div class="control-group">


          <h3>
            <span class="label label-info">待抓取的微博时间范围</span>

            <input name="span" type="text" placeholder="day" class="input-xlarge"></h3>

        </div>
 -->
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
</div>
%rebase layout
