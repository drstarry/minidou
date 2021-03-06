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
        <div class="col-md-3">

            <!-- <a class="btn btn-primary btn-lg" role="button pull-right" data-toggle="modal" href='#myModal'><i class="fa fa-upload"></i> Upload
            </a> -->
                %if msg:
                <h2><span class="label label-success">Successfully uploaded {{msg}}</span></h2>
                %end

                    <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" style="overflow-y: hidden;">
                        <div class="modal-dialog">
                            <div class="modal-content">

                            <form onsubmit="refearsh()" enctype="multipart/form-data"  method="post" action="/upload_event">
                                <div class="modal-header">
                                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                    <h4 class="modal-title" id="myModalLabel">choose the file you want to upload</h4>
                                </div>
                                   <div class="modal-body">

                                        <input name="file" value="Search local files" type="file"  accept="text/txt, text/bat, text/csv"/>


                                   </div>
                                <div class="modal-footer">
                                    <input type="submit"  class="btn btn-success"  value="Submit"/>
                                    <button type="button" class="btn btn-danger" data-dismiss="modal">cancel</button>
                                </div>
                            </form>
                            </div><!-- /.modal-content -->
                        </div><!-- /.modal-dialog -->
                    </div><!-- /.modal -->

          <h2>Map of events </h2>
          <p>This is an interactive events map of Beijing city</p><p>Click the marker to see the detailed info</p>



        </div>



        <div class="col-lg-9" >
        <div id="map" style="width: 850px; height: 800px"></div>
        </div>
    </div>

<script src="/static/vis_data/data.js"></script>

<script>
        var map = L.map('map').setView([39.5548, 116.2400], 14);
        mapLink =
            '<a href="http://openstreetmap.org">OpenStreetMap</a>';
        L.tileLayer(
            'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; ' + mapLink,
            maxZoom: 18,
            }).addTo(map);
        var marker;
        var lat,lon;
        var addr,time,title;

        for (var i = 0; i < data.length; i++) {
            var popstr = '';
            lat = data[i][0];
            lon = data[i][1];
            info = data[i][2];

            for (var j = 0; j < info.length; j++)
            {
                popstr += "<b>"+ info[j][0] +"</b></br>"+ info[j][1] +"</br>"+info[j][2] + "</br>";
            }

            marker = new L.marker([lat, lon])
                        .addTo(map)
                        .bindPopup(popstr)
                        .openPopup();

        }

</script>

%rebase layout
