<style type="text/css">
  form.form-inline {
    display: inline-block;
  }
</style>


<div class="row">
    <div class="col-md-4">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h2>
                   <img src="http://img3.douban.com/favicon.ico" height="55px" weidth="55px"></img>
                Douban events|豆瓣同城活动
            </h2>
            </div>
            <div class="panel-body">
                <h4>
                    <b>Type|类型: </b>{{etype}}
                </h4>
                <h4>
                    <b>Time span|时间段: </b>{{etime}}
                </h4>


                <h4>

                </h4>

                    <p><a href="/images/sampledocs/9/File-Download-HTML.txt" class="dv_dl_block" id="gatSampleTxt1" target="_blank" rel="nofollow"></a>
                   

                    <p><a class="btn btn-primary btn-lg" href="/vis_events" role="button pull-right" target="_blank" rel="nofollow"><i class="fa fa-arrow-right"></i> Events map
                    </a>

            </div>
        </div>
    </div>

    <div class="col-md-8">
        %for e in events:
          <div class="row featurette">
              <div class="col-md-5">
                 <h2 class="featurette-heading">{{e['title']}}</h2>
                 <!--  <img src="{{e['pic']}}" width ="110px"></img> -->
              </div>
              <div class="col-md-7">
                  <!-- <h4 class="featurette-heading">{{e['title']}}</h4> -->
                  %if e['tags'] != []:
                        %for tag in e['tags']:
                        <span class="label label-info">{{tag}}</span>
                        %end
                  %end
                  <h4 class="text-muted">{{e['etime']}}</h4>
                  <h4 >{{e['loc']}}</h4>
                  <h4><span>Fee | 费用: </span>
                  %for f in e['fee']:
                  <span >{{f}}</span></h4>
                  %end
                  </br>
                  <h5><span class="label label-danger">Like | 喜欢 {{e['like_count']}}</span>
                  <span class="label label-warning">Go | 参与 {{e['go_count']}}</span></h5>
                  <a class="btn btn-default btn-lg pull-right" role="button" href="{{e['href']}}">Detail | 详情 »</a>

                  <p class="lead"></p>
              </div>
          </div>
             <hr class="featurette-divider">
        %end

    </div>

</div>

      <footer>
        <p class="pull-right"><a href="#">Back to top</a></p>

      </footer>
%rebase layout
