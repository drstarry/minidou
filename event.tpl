<style type="text/css">
  form.form-inline {
    display: inline-block;
  }
</style>

<div class="row">
    <div class="col-md-5">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h2>
                    <img src="static/img/city.jpg"></img>
                豆瓣同城活动抓取
            </h2>
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
        <form class="form-horizontal" enctype="multipart/form-data" method="post" action="/crawl/event">
            <fieldset>
                <div id="legend" class="">
                    <legend> <i class="fa fa-gear fa-2x pull-left"></i>
                        爬虫参数设置：
                    </legend>
                </div>

                <div class="control-group">

                    <!-- Text input-->

                    <h3>
                        <span class="label label-info">活动类别</span>

                        <select class="form-control">
                            <option>1.音乐</option>
                            <option>2.戏剧</option>
                            <option>3.讲座</option>
                            <option>4.电影</option>
                            <option>5.全部</option>
                        </select>


                    </h3>
                    <p class="help-block">注意:尽量不要选全部，要抓很久哦，可不是程序挂掉了哦</p>
                </div>

                <div class="control-group">

                    <!-- Select Basic -->
                    <h3>
                        <span class="label label-info">活动时间</span>

                        <select class="form-control">
                            <option>1.今天</option>
                            <option>2.明天</option>
                            <option>3.周末</option>
                            <option>4.最近一周</option>
                            <option>5.选择日期</option>
                        </select>

                    <p class="help-block">提示:同样奉劝不要选全部，要抓很久，可不是挂了哦</p>
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
