<style type="text/css">
  form.form-inline {
    display: inline-block;
  }
</style>

<div class="row">
  <div class="col-md-5">
    <div class="panel panel-default">
      <div class="panel-heading">
      <h2> <img src="http://img3.douban.com/favicon.ico"></img>豆瓣同城活动抓取</h2>
    </div>
    <div class="panel-body">
      <h4>
        请输入您想要抓取活动 <b>类型</b>
        和活动 <b>时间范围</b>
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
    <form class="form-horizontal" enctype="multipart/form-data" method="post" action="/crawl">
      <fieldset>
        <div id="legend" class="">
          <legend> <i class="fa fa-gear fa-2x pull-left"></i>
            爬虫参数设置：
          </legend>
        </div>

        <div class="control-group">

          <!-- Text input-->

          <h3>
            <span class="label label-info">待爬取用户ID</span>

            <input name="id" type="text" placeholder="id" class="input-xlarge">
            <span class="label label-warning">eg.karentse</span>
          </h3>
          <p class="help-block">注意:id不是用户名，用户名可以有重复，而id是每个用户的唯一凭证哦</p>
        </div>

        <div class="control-group">

          <!-- Select Basic -->
          <h3>
            <span class="label label-info">用户关系的节点度数</span>

            <input name="degree" type="text" placeholder="degree" class="input-xlarge"></h3>
          <p class="help-block">提示:我们把和该用户直接相连的邻居节点度数设为1，依此类推</p>
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
