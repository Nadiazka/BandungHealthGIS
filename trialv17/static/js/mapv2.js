$(document).ready(function(){
    console.log("Ready");
    var pnykt;

/*
    $(document).on('submit', 'filter', function(){
        $.ajax({
            url: "{% url 'PuskesmasView2' %}",
            type:'POST',
            data: {nama_pkm:$(this).val()},
        })
        .done(function(response){
            console.log(response);
        })
        .fail(function(response){
            console.log("Failed")
        })
    })

*/
    $("#filter").submit(function(){
        console.log("Wilayah Aman");
        $.ajax({
            url: "/PuskesmasView2/", /* URL hasil */
            type:'POST',
            data:{
                nama_pkm:$('#InputWlyh').val(),
                penyakit:$('#InputPnykt').val(),
                gender:$('#InputGender').val(),
                umurStart:$('#InputUmurStart').val(),
                umurEnd:$('#InputUmurEnd').val(),
                dateStart:$('#dateStart').val(),
                dateEnd:$('#dateEnd').val(),
                jenisKasus:$('#InputJenisKasus').val(),
            },
        })
        .done(function(response){
            console.log(response);
            console.log("Masuk Pak Haji");
        })
        .fail(function(response){
            console.log("Failed");
        })
    })

/*Puskesmas*/
    var pkm = $.ajax({
                url: "https://raw.githubusercontent.com/Nadiazka/TugasAkhir/master/trialv12/data/puskesmas_area_pure.geojson",
                dataType: "json",
                success: console.log("Puskesmas data successfully loaded."),
                error: function(xhr) {
                    alert(xhr.statusText)
                }
            })
            $.when(pkm).done(function() {
                var map = L.map('petabandung')
                    .setView([-6.914744, 107.60981], 12);

                var basemap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                    { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    subdomains: 'abcd',
                    maxZoom: 19
                }).addTo(map);
                // Add requested external GeoJSON to map
                var LayerPuskesmas = L.geoJSON(pkm.responseJSON).addTo(map);

                function getColor(d) {
                        return d > 200  ? '#800026' :
                                d > 100 ? '#BD0026' :
                                d > 50  ? '#E31A1C' :
                                d > 25  ? '#FC4E2A' :
                                d > 10  ? '#FD8D3C' :
                                d > 5   ? '#FEB24C' :
                                         '#FFEDA0';
                    }
                //Kotak Info
                var info = L.control();

                    info.onAdd = function (map) {
                        this._div = L.DomUtil.create('div', 'info');
                        this.update();
                        return this._div;
                    };

                    info.update = function (props) {
                        this._div.innerHTML = '<h6>Sakit Hati</h6>';
                    };

                    info.addTo(map);

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

            });
            
    /*Kecamatan*/


})

    