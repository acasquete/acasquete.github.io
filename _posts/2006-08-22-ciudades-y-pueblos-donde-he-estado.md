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
}
</script>