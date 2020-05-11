$(document).ready(function(){
	// get data
  URLDataPkm="https://raw.githubusercontent.com/Nadiazka/TugasAkhir/master/trialv12/data/DataPuskesmasv5.json";
  // load GeoJSON from an external file
  URLpkm = "https://raw.githubusercontent.com/Nadiazka/TugasAkhir/master/trialv12/data/areaPkm.geojson";

  var dataPuskesmas = {} ;
  $.getJSON(URLDataPkm, 
      function(data) {    
          for (var i = 0; i < data.length; i++) {
              dataPuskesmas[data[i].kode] = {"area" : data[i].Name, "kasus" : data[i].kasus};
          };
      }
  );

  // initialize the map
  var map = L.map('map').setView([-6.914744, 107.60981], 12);

  // load a tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

 //Hover Control
  var info = L.control();

  info.onAdd = function (map) {
      this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
      this.update();
      return this._div;
  };

  // method that we will use to update the control based on feature properties passed
  info.update = function (props) {
      this._div.innerHTML = '<h4>Bandung Health GIS</h4>' +  (props ?
          '<b>' + props.Name + '</b><br />' + dataPuskesmas[props.kode_kode].kasus + ' kasus'
          : 'Dekatkan mouse untuk melihat jumlah kasus');
  };

  info.addTo(map);

  function getColor(d) {
          return d > 200  ? '#800026' :
                  d > 100 ? '#BD0026' :
                  d > 50  ? '#E31A1C' :
                  d > 25  ? '#FC4E2A' :
                  d > 10  ? '#FD8D3C' :
                  d > 5   ? '#FEB24C' :
                           '#FFEDA0';
      }
  
  function style(feature) {
    return {
          fillColor: getColor(dataPuskesmas[feature.properties.kode_kode].kasus),
          weight: 2,
          opacity: 1,
          color: 'white',
          dashArray: '3',
          fillOpacity: 0.7
      };
  }

  function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
      }
    info.update(layer.feature.properties);
  }

  
  function resetHighlight(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    });

    info.update();
  }

  function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
  }

  function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
  }

  $.getJSON(URLpkm,function(data){
    L.geoJson(data, {
    style: style,
    onEachFeature: onEachFeature
    }).addTo(map);
  });


  //Legenda
  var legend = L.control({position: 'bottomright'});

      legend.onAdd = function (map) {

          var div = L.DomUtil.create('div', 'info legend'),
              grades = [0, 5, 10, 25, 50, 100, 200, 500],
              labels = [],
              from, to;

          for (var i = 0; i < grades.length; i++) {
              from = grades[i];
              to = grades[i + 1];

              labels.push(
                  '<i style="background:' + getColor(from + 1) + '"></i> ' +
                  from + (to ? '&ndash;' + to : '+'));
          }

          div.innerHTML = labels.join('<br>');
          return div;
      };

      legend.addTo(map);


})


