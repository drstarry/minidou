<style type="text/css">
  form.form-inline {
    display: inline-block;
  }
  .transbox
  {
   /*display:none;*/
  height:100%;
  width:100%;
  background-color:red;
  opacity:0.6;
  z-index:10000;

  }

</style>


    <div class="col-md-5">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h2>
                   <img src="http://img3.douban.com/favicon.ico" height="55px" weidth="55px"></img>
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
            <form class="form-horizontal" onSubmit="winload()" enctype="multipart/form-data" method="post" action="/crawl/event">
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

                            <select name="etype" class="form-control">
                                <option>1.音乐</option>
                                <option>2.戏剧</option>
                                <option>3.讲座</option>
                                <option>4.聚会</option>
                                <option>5.电影</option>
                                <option>6.展览</option>
                                <option>7.运动</option>
                                <option>8.公益</option>
                                <option>9.旅行</option>
                                <option>10.全部</option>
                            </select>
                        </h3>
                        <p class="help-block">注意:尽量不要选全部，要抓很久哦</p>
                    </div>

                    <div class="control-group">

                        <!-- Select Basic -->
                        <h3>
                            <span class="label label-info">活动时间</span>

                            <select name="etime" class="form-control">
                                <option>1.今天</option>
                                <option>2.明天</option>
                                <option>3.周末</option>
                                <option>4.最近一周</option>
                                <option>5.选择日期</option>
                            </select></h3>

                        <p class="help-block">提示:同样奉劝不要选全部，要抓很久哦</p>
                    </div>


                <div class="control-group">
                    <label class="control-label"></label>

                    <!-- Button -->
                    <div class="controls">
                        <input type="submit" class="btn btn-success" onclick="show()" value="开始"></div>
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
