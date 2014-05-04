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
			<a class="btn btn-primary btn-lg" role="button pull-right" data-toggle="modal" href='#myModal'><i class="fa fa-upload"></i> 上传
            </a>
            %if msg != 'none':
            <span>您上传了{{msg}}</span>
            %end
                    <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" style="overflow-y: hidden;">
                        <div class="modal-dialog">
                            <div class="modal-content">

                            <form onsubmit="refearsh()" enctype="multipart/form-data"  method="post" action="/upload_ana">
                                <div class="modal-header">
                                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                    <h4 class="modal-title" id="myModalLabel">请选择您要上传的文件</h4>
                                </div>
                                   <div class="modal-body">

                                        <input name="file" value="查看本地文件" type="file"  accept="text/txt, text/bat, text/csv"/>


                                   </div>
                                <div class="modal-footer">
                                    <input type="submit"  class="btn btn-success"  value="确认"/>
                                    <button type="button" class="btn btn-danger" data-dismiss="modal">取消</button>
                                </div>
                            </form>
                            </div><!-- /.modal-content -->
                        </div><!-- /.modal-dialog -->
                    </div><!-- /.modal -->
		</div>



        <div class="col-lg-8" >
        <iframe src="/" height="600px" width="800px" scrolling="no">


        </iframe>
        </div>
    </div>



%rebase layout
