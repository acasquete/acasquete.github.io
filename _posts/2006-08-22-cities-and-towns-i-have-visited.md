---
title: Cities and towns I have visited
tags: [personal]
reviewed: true
header_fullview: world-map-2.jpg
---
Using the Google Maps API, I have created this map where I have marked (and will continue to mark) all the cities and towns I have visited and spent at least one night.

<div id="map" style="width:100%; height: 400px"></div>

<script
      src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCHq3yNM4mSpvgccI8wNdXMVoI8j_dKKKk&callback=initMap&v=weekly" async></script>
    
<script>
let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 41.371672, lng: 2.130554 },
    
    zoom: 6,
  });
  
  {% for city in site.data.cities %}
  new google.maps.Marker({ position: { lat: {{city.lat}}, lng: {{city.long}} }, map, title: "{{city.name}}" });
  {% endfor %}

}
</script>