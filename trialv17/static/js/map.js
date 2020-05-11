//Ambil data
var loc_pkm = ''
var data = ''//ini nanti pokoknya localhost/8000/?search= <Penyakit>?q= <umur>?q=<periode>

URLpkmv2 = 'https://raw.githubusercontent.com/Nadiazka/TugasAkhir/master/trialv12/data/puskesmas_area_pure.geojson'
var area_pkm = $.ajax({
            url: URLpkmv2,
            dataType: "json",
            success: console.log("Puskesmas data successfully loaded."),
            error: function(xhr) {
                alert(xhr.statusText)
            }
        })

//Peta dasar
var petabandung = L.map('petabandung')
                .setView([-6.914744, 107.60981], 12);
/*
var petabandung = L.map(
                "petabandung",
                {
                    center: [-6.914744, 107.60981],
                    crs: L.CRS.EPSG3857,
                    zoom: 12,
                    zoomControl: true,
                    preferCanvas: false,
                }
            );
*/
var basemap = L.tileLayer(
                'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(petabandung);

//Setting peta
    function getColor(d) {
        return d > 1000 ? '#800026' :
                d > 500  ? '#BD0026' :
                d > 200  ? '#E31A1C' :
                d > 100  ? '#FC4E2A' :
                d > 50   ? '#FD8D3C' :
                d > 20   ? '#FEB24C' :
                d > 10   ? '#FED976' :
                            '#FFEDA0';
    }

    function style(feature) {
        return {
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7,
            fillColor: getColor(feature.properties.density)
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

    var geojson;

    function resetHighlight(e) {
        geojson.resetStyle(e.target);
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

//Add setting ke peta area puskesmas
URLpkm = 'https://raw.githubusercontent.com/Nadiazka/TugasAkhir/master/trialv17/data/peta.js'

//geojson = L.geoJson(dataPeta).addTo(petabandung);

//var layer_pkm = L.geoJSON(area_pkm.responseJSON).addTo(petabandung);


$.getJSON("URLpkmv2", function(data) {
    L.geoJson(data, {
        style: myStyle
    }).addTo(map);
})

//{style: style,onEachFeature: onEachFeature}
//Add setting ke peta kecamatan

//Layer kontrol

//Kotak Info
var info = L.control();

    info.onAdd = function (petabandung) {
        this._div = L.DomUtil.create('div', 'info');
        this.update();
        return this._div;
    };

    info.update = function (props) {
        this._div.innerHTML = '<h6>Sakit Hati</h6>';
    };

    info.addTo(petabandung);

//Legenda
var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (petabandung) {

        var div = L.DomUtil.create('div', 'info legend'),
            grades = [0, 10, 20, 50, 100, 200, 500, 1000],
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

    legend.addTo(petabandung);