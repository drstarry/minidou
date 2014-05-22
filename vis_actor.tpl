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
            <!-- <a class="btn btn-primary btn-lg" role="button pull-right" data-toggle="modal" href='#myModal'><i class="fa fa-upload"></i> 上传
            </a> -->
                %if msg:
                <h2><span class="label label-success">您成功上传了{{msg}}</span></h2>
                %end

                    <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" style="overflow-y: hidden;">
                        <div class="modal-dialog">
                            <div class="modal-content">

                            <form onsubmit="refearsh()" enctype="multipart/form-data"  method="post" action="/upload_actor">
                                <div class="modal-header">
                                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                    <h4 class="modal-title" id="myModalLabel">请选择您要上传的文件</h4>
                                </div>
                                   <div class="modal-body">

                                        <input name="file" value="查看本地文件" type="file"  />


                                   </div>
                                <div class="modal-footer">
                                    <input type="submit"  class="btn btn-success"  value="确认"/>
                                    <button type="button" class="btn btn-danger" data-dismiss="modal">取消</button>
                                </div>
                            </form>
                            </div><!-- /.modal-content -->
                        </div><!-- /.modal-dialog -->
                    </div><!-- /.modal -->


        <h2>演员合作分布 </h2>
          <p>这是一个演员合作关系力导引图 </p><p>您可以移动鼠标显示演员姓名，或者任意拖拽这些点</p><p>


        </div>



        <div class="col-lg-8" >
        <iframe src="/coactor" height="600px" width="600px" scrolling="no">


        </iframe>
        </div>
    </div>



%rebase layout
