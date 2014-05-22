   <div class="col-md-5">
          <img src="{{img}}" alt="{{movie['title']}}" height="148px" width="100px" >
          <h2>{{movie['title']}}</h2>
          <p>{{movie['year']}}</p>
              <p>导演:</p>

              %for d in movie['director']:
              <span class="label label-info">{{d}}</span>
              %end
              <hr class="featurette-divider">
              <p>编剧:</p>
              %for b in movie['bianju']:
              <span class="label label-info">{{b}}</span>
              %end
             <hr class="featurette-divider">
              <p>演员:</p>
              %for a in movie['actors']:
              <span class="label label-info">{{a['name']}}</span>
              %end
        </p>
       <hr class="featurette-divider">
      <p><a href="/images/sampledocs/9/File-Download-HTML.txt" class="dv_dl_block" id="gatSampleTxt1" target="_blank" rel="nofollow"></a>
                    <a class="btn btn-primary btn-lg" href="/lib/data/actors.txt" role="button pull-right" target="_blank" rel="nofollow"><i class="fa fa-download"></i> 下载
                    </a>
                    <hr class="featurette-divider">
                    <p><a class="btn btn-primary btn-lg" href="/vis_actor" role="button pull-right" target="_blank" rel="nofollow"><i class="fa fa-arrow-right"></i> 演员合作关系
                    </a>
                    <hr class="featurette-divider">
                    <p><a class="btn btn-primary btn-lg" href="/vis_review" role="button pull-right" target="_blank" rel="nofollow"><i class="fa fa-arrow-right"></i> 影评关键词
                    </a>

    </div><!-- /.col-lg-4 -->

   <div class="col-md-7">
    <h2>影评:</h2>
        %for r in review:
        <h3><a href='{{r['href']}}'>{{r['title']}}</a></h3>
        <h4>{{r['bd_short']}}</h4>
        <hr class="featurette-divider">
        %end
   </div>

 <footer>
        <p class="pull-right"><a href="#">Back to top</a></p>

      </footer>
%rebase layout
