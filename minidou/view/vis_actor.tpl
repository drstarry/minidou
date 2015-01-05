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
	
            <!-- <a class="btn btn-primary btn-lg" role="button pull-right" data-toggle="modal" href='#myModal'><i class="fa fa-upload"></i> upload
            </a> -->
                %if msg:
                <h2><span class="label label-success">You successfully {{msg}}</span></h2>
                %end

                    <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" style="overflow-y: hidden;">
                        <div class="modal-dialog">
                            <div class="modal-content">

                            <form onsubmit="refearsh()" enctype="multipart/form-data"  method="post" action="/upload_actor">
                                <div class="modal-header">
                                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                    <h4 class="modal-title" id="myModalLabel">choose the file you want to upload</h4>
                                </div>
                                   <div class="modal-body">

                                        <input name="file" value="Search local" type="file"  />


                                   </div>
                                <div class="modal-footer">
                                    <input type="submit"  class="btn btn-success"  value="Submit"/>
                                    <button type="button" class="btn btn-danger" data-dismiss="modal">cancel</button>
                                </div>
                            </form>
                            </div><!-- /.modal-content -->
                        </div><!-- /.modal-dialog -->
                    </div><!-- /.modal -->


        <h2>co-actor network </h2>
          <p>This is a co-actor network of the movie you choose </p>
</br>
<a class="btn btn-primary btn-lg" href="/static/vis_data/actor.json" role="button pull-right" target="_blank" rel="nofollow"><i class="fa fa-download"></i> Download
                    </a>
</br>
        </div>



        <div class="col-lg-8" >
        <iframe src="/coactor" height="600px" width="600px" scrolling="no">


        </iframe>
        </div>
    </div>



%rebase layout
