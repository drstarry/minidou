
<style type="text/css">

        .col-lg-8 {

          height: 100%;

        }


</style>

<div class="col-lg-4">
    <a class="btn btn-primary btn-lg" role="button pull-right" data-toggle="modal" href='#myModal'> <i class="fa fa-upload"></i>
        上传
    </a>
    %if msg != 'none':
    <p>
        <span class="label label-success">您上传了{{msg}}</span>
    </p>
    %end
    <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" style="overflow-y: hidden;">
        <div class="modal-dialog">
            <div class="modal-content">
                <form onsubmit="refearsh()" enctype="multipart/form-data"  method="post" action="/upload_vis">
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

            </div>
            <!-- /.modal-content --> </div>
        <!-- /.modal-dialog --> </div>
    <!-- /.modal -->

</div>

<div class="col-lg-8" >
    <iframe src="/map" height="600px" width="800px" scrolling="no"></iframe>
</div>
%rebase layout
