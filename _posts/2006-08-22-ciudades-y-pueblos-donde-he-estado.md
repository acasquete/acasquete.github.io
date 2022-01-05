---
title: Ciudades y pueblos donde he estado
tags: [random]
---
Aprovechando la API de Google Maps he creado este mapa donde he marcado (y seguiré marcando) todas las ciudades y pueblos que he visitado.

<div id="map" style="width:100%; height: 400px"></div>

<script
      src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCHq3yNM4mSpvgccI8wNdXMVoI8j_dKKKk&callback=initMap&v=weekly"
      async
    ></script>
    
<script>
let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    
    zoom: 8,
  });

  map.setMapType(map.mapTypes[0]);
    map.addControl(new GMapTypeControl());
    map.addControl(new GLargeMapControl());
	map.addControl(new GScaleControl());
	
	 map.centerAndZoom(new GPoint(2.130554, 41.371672), 12);

   
    map.addOverlay(createMarker(new GPoint(  2.130554,  41.371672), "Barcelona<br>Home SWEET Home")); 
    map.addOverlay(createMarker(new GPoint( -3.689518,  40.437671), "Madrid"));
    map.addOverlay(createMarker(new GPoint(  2.816277,  41.977486), "Girona"));
    map.addOverlay(createMarker(new GPoint(  2.967167,  42.266639), "Figueres"));
    map.addOverlay(createMarker(new GPoint(  3.877831,  43.608239), "Montpellier"));
    map.addOverlay(createMarker(new GPoint(  5.379181,  43.329548), "Marseille"));
    map.addOverlay(createMarker(new GPoint(-58.407097, -34.625863), "Buenos Aires"));
    map.addOverlay(createMarker(new GPoint(-43.183651, -22.965506), "Rio de Janeiro"));
    map.addOverlay(createMarker(new GPoint(-46.632328, -23.532514), "S�o Paulo"));
    map.addOverlay(createMarker(new GPoint(-45.458078, -23.819898), "Maresias"));
    map.addOverlay(createMarker(new GPoint(-64.188995, -31.404345), "C�doba"));
    map.addOverlay(createMarker(new GPoint(-68.831406, -32.891696), "Mendoza"));
    map.addOverlay(createMarker(new GPoint(-60.658264, -32.956825), "Rosario"));
    map.addOverlay(createMarker(new GPoint(-58.519363, -33.011255), "Gualeguaychu"));
    map.addOverlay(createMarker(new GPoint(-61.253500, -32.848010), "Correa"));
    map.addOverlay(createMarker(new GPoint(-54.581108, -25.540893), "Foz do Igua�u"));
    map.addOverlay(createMarker(new GPoint( -2.935195,  43.262831), "Bilbao"));
    map.addOverlay(createMarker(new GPoint( -0.880966,  41.652778), "Zaragoza"));
    map.addOverlay(createMarker(new GPoint( -0.407395,  42.138968), "Huesca"));
    map.addOverlay(createMarker(new GPoint( -0.546312,  42.573057), "Jaca"));
    map.addOverlay(createMarker(new GPoint( -1.105800,  40.343371), "Teruel"));
    map.addOverlay(createMarker(new GPoint(-39.708366, -18.420336), "Ita�nas"));
    map.addOverlay(createMarker(new GPoint( -0.382805,  39.466945), "Val�ncia"));
    map.addOverlay(createMarker(new GPoint( -0.350747,  39.498875), "Alboraya"));
    map.addOverlay(createMarker(new GPoint( -0.221272,  39.660487), "Port de Sagunt"));
    map.addOverlay(createMarker(new GPoint( -0.466232,  39.436458), "Torrent"));
    map.addOverlay(createMarker(new GPoint( -0.139389,  38.548568), "Benidorm"));
    map.addOverlay(createMarker(new GPoint( -4.406869,  36.721067), "M�laga"));
    map.addOverlay(createMarker(new GPoint( -3.594675,  37.171602), "Granada"));
    map.addOverlay(createMarker(new GPoint( -4.780083,  37.889893), "C�rdoba"));
    map.addOverlay(createMarker(new GPoint( -4.322777,  37.617155), "Baena"));
    map.addOverlay(createMarker(new GPoint( -2.138386,  40.076627), "Cuenca"));
    map.addOverlay(createMarker(new GPoint(  5.054398,  43.406419), "Martigues"));
    map.addOverlay(createMarker(new GPoint( -4.117899,  40.947832), "Segovia"));
    map.addOverlay(createMarker(new GPoint( -5.657959,  40.968039), "Salamanca"));
    map.addOverlay(createMarker(new GPoint( -5.001011,  41.501635), "Tordesillas"));
    map.addOverlay(createMarker(new GPoint( -4.026833,  39.860472), "Toledo"));
    map.addOverlay(createMarker(new GPoint(  1.582375,  42.535501), "Encamp"));
    map.addOverlay(createMarker(new GPoint(  1.530018,  42.508299), "Andorra la Vella"));
    map.addOverlay(createMarker(new GPoint(  0.740633,  42.407805), "El Pont de Suert"));
    map.addOverlay(createMarker(new GPoint(  2.850008,  41.700282), "Lloret de Mar"));
    map.addOverlay(createMarker(new GPoint(  1.140175,  41.076375), "Salou"));
    map.addOverlay(createMarker(new GPoint(  1.106615,  41.155523), "Reus"));
    map.addOverlay(createMarker(new GPoint(  2.900219,  42.697829), "Perpignan"));
    map.addOverlay(createMarker(new GPoint(  2.342749,  43.218500), "Carcassonne"));
    map.addOverlay(createMarker(new GPoint(  0.932293,  41.633471), "Golm�s"));
    map.addOverlay(createMarker(new GPoint(-64.428446, -31.656252), "Alta Gracia"));   
    map.addOverlay(createMarker(new GPoint(-64.496956, -31.420387), "Carlos Paz"));   
    map.addOverlay(createMarker(new GPoint(-68.328094, -34.618517), "San Rafael"));
    map.addOverlay(createMarker(new GPoint(  1.929817,  42.436491), "Puigcerd�"));
    map.addOverlay(createMarker(new GPoint(  1.131420,  42.412051), "Sort"));
    
   
  
    	 
	map.addOverlay(new GPolyline([new GPoint(  2.083497,  41.298992), new GPoint( 4.756737,  52.312204), new GPoint( -46.474228, -23.431985)], "#00ff00", 2));
	map.addOverlay(new GPolyline([new GPoint(  2.083497,  41.298992), new GPoint( 8.556633,  50.039722), new GPoint( -43.251543, -22.815824), new GPoint( -46.474228, -23.431985), new GPoint( -58.538418, -34.814508)], "#0000ff", 2));
	}
}
</script>