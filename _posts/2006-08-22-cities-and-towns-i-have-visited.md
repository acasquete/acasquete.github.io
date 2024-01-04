---
title: Cities and towns I have visited
tags: [personal]
reviewed: true
header_fullview: world-map-2.jpg
---
Discover my journey through the Google Maps API: a map where I've marked every city and town where I've spent at least one night. This map is more than just locations; it's a story of my travels, a visual diary of the places I've explored. Follow along as I continue to add new destinations, each with its own unique tale.

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