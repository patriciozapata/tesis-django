var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        osm = L.tileLayer(osmUrl, { maxZoom: 18, attribution: osmAttrib }),
        map = new L.Map('map', { center: new L.LatLng(10.505, -90.04), zoom: 3 }),
        drawnItems = L.featureGroup().addTo(map);
L.control.layers(
  {
    'osm': osm.addTo(map),
    "google": L.tileLayer('http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}', {attribution: 'google'})
  },
  {'drawlayer': drawnItems},
  {
    position: 'topleft',
    collapsed: false
  }
).addTo(map);
var MapControlDraw = new L.Control.Draw(
  {
    edit: {
      featureGroup: drawnItems,
      poly: {
        allowIntersection: false
      }
    },
    draw: {
      polygon: {
        allowIntersection: false,
        showArea: true
      }
    }
  }
);
$("#data").hide();
$("#freg").hide();
var freg = document.getElementById("freg");
map.on(L.Draw.Event.CREATED, function (event) {
    var layer = event.layer;
    drawnItems.addLayer(layer);
    layer = layer.toGeoJSON();
    var coords = layer.geometry.coordinates;
    var nameLayer = document.getElementById("geoname").value;
    $("#freg").hide("slide", 1000);
});
function showCoords(coords) {
  var data = document.getElementById("data");
  var tablaCoord = document.getElementById("descripcion");
  if(data.style.display != "none"){
    $("#data").hide("slide", 1000);
    $("#descripcion").empty();
  }else{
    $("#data").show("slide", 1000);
    $("#descripcion").empty();
  }
  var lstCoord =  coords.toString().split(",");
  lstCoord.forEach(function(coord, index){
    if(index % 2){
      var td = document.createElement("td");
      td.setAttribute("class", "column2");
      tr = tablaCoord.rows[tablaCoord.rows.length-1];
      tr.setAttribute("class", "");
      td.innerHTML = coord;
      tr.appendChild(td);
    }else{
      var tr = document.createElement("tr");
      var td = document.createElement("td");
      td.setAttribute("class", "column1");
      tr.appendChild(td);
      tablaCoord.appendChild(tr);
      td.innerHTML = coord;
    }
  });
};
map.on('draw:drawstart', function() {
  if(freg.style.display == "none"){
    $("#freg").show("slide", 1000);
  }
});
map.on('draw:edited', function (e) {
  var fg = [];
  var layers = e.layers.toGeoJSON();
  var features = layers.features;
  features.forEach(function ejecuta(feature) {
    var temp={'id': feature.properties.pk, 'nombre':feature.properties.name, 'geom': feature.geometry};
    fg.push(temp);
  })
  var parametrosR = {
    datos: JSON.stringify(fg),
  };
  $.ajax({
    url: 'actualizar',
    type: 'post',
    data: parametrosR,
    error: function(){
      alert("Ocurrio un error en la Modificación.");
    },
    success: function(data){
      alert(data);
    }
  });
});
function cargaLayers(map, options){
  var datasets = new L.GeoJSON.AJAX("{% url 'carto:Data2' %}", {
    onEachFeature: function(feature, layer){
      drawnItems.addLayer(layer);
      layer.on("click", function(e){
        showCoords(feature.geometry.coordinates);
      })
    }
  });
}
function iniciarRegistro(){
  var nombreCapa = document.getElementById("txtNombreCapa");
  alert(nombreCapa.value);
  if(nombreCapa.value != ""){
    nombreCapa.readOnly = true;
    map.addControl(MapControlDraw);
  }else{
    if(confirm("¿Desea continuar sin un nombre?")){
      map.addControl(MapControlDraw);
    }
  }
}
function regNombre(e){
  e.src = "{% static 'img/custom/xmas_bawi_i00.png' %}"
  $("#add2").show("slide",1000);
}
function respaldo(){
  map.removeControl(MapControlDraw);
  map.addControl(MapControlDraw);
}
cargaLayers(map);
