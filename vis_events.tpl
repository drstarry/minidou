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
            <a class="btn btn-primary btn-lg" role="button pull-right" data-toggle="modal" href='#myModal'><i class="fa fa-upload"></i> 上传
            </a>

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



        <div class="col-lg-9" >
        <div id="map" style="width: 850px; height: 800px"></div>
        </div>
    </div>
<script src="/static/vis_data/data.js"></script>
<script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?sensor=false"></script>
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
        var geocoder = new google.maps.Geocoder();
        var lat,lon;
        var popstr;
        var addr;

        for (var i = 0; i < data.length; i++) {
            console.log(i);

            var es = data[i][2];
            for (var j = 0; j<es.length; j++)
            {
                popstr += "<b>"+es[j][0]+"</b></br>"+es[j][1]+"</br>"+es[j][2]+"</br>";
            }
            // popstr = data[i].length;
            console.log(popstr);
            marker = new L.marker([lat,lon])
                .addTo(map)
                .bindPopup(popstr)
                .openPopup();
            // marker = new L.circle([data[i][0], data[i][1]], 2500,
            //     {title: popstr},
            //     {
            //         color: 'red',
            //         fillColor: '#f03',
            //         fillOpacity: 0.6
            //     })
            //     .addTo(map);
            //     // .bindPopup(popstr)
            //     // .openPopup();
        }

</script>

%rebase layout
