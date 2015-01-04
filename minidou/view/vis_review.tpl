<style type="text/css">
    form.form-inline {
        display: inline-block;
    }


    .link {
      stroke: #ccc;
    }

    .node text {
      pointer-events: none;
      font: 10px sans-serif;
    }


</style>


<div class="row">
        <div class="col-md-4">

          <h2>Word clouds of movie review</h2>
          <p>from the reviews you choose</p>

            <hr class="featurette-divider">

            <h2>You can upload your own text</h2>
            <a class="btn btn-primary btn-lg" role="button pull-right" data-toggle="modal" href='#myModal'><i class="fa fa-upload"></i> upload
            </a>
                %if msg:
                <h2><span class="label label-success">Successfully uploaded{{msg}}</span></h2>
                <a class="btn btn-primary btn-lg" href='/vis_review'><i class="fa fa-arrow-right"></i> show
            </a>
                %end
                    <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" style="overflow-y: hidden;">
                        <div class="modal-dialog">
                            <div class="modal-content">

                            <form onsubmit="refearsh()" enctype="multipart/form-data"  method="post" action="/upload_review">
                                <div class="modal-header">
                                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                    <h4 class="modal-title" id="myModalLabel">choose the file you want to upload</h4>
                                </div>
                                   <div class="modal-body">

                                        <input name="file" value="查看本地文件" type="file"  accept="text/txt, text/bat, text/csv"/>


                                   </div>
                                <div class="modal-footer">
                                    <input type="submit"  class="btn btn-success"  value="确认"/>
                                    <button type="button" class="btn btn-danger" data-dismiss="modal">cancel</button>
                                </div>
                            </form>
                            </div><!-- /.modal-content -->
                        </div><!-- /.modal-dialog -->
                    </div><!-- /.modal -->
        </div>



        <div class="col-lg-8" >
        <iframe src="/words" height="600px" width="600px" scrolling="no">


        </iframe>
        </div>
    </div>



%rebase layout
