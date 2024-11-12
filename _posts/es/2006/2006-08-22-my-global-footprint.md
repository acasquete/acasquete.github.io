---
title: My Global Footprint
tags: [personal]
reviewed: true
header_fullview: world-map-2.jpg
---
Discover my journey through the Google Maps API: a map where I've marked every city and town where I've spent at least one night. This map is more than just locations; it's a story of my travels, a visual diary of the places I've explored. Follow along as I continue to add new destinations, each with its own unique tale.

<div id="map" style="width:100%; height: 400px"></div>

<script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAGXUKzypxUeI8MBKygbYY_0UGm-NDkBk0&callback=initMap&v=weekly&libraries=marker"></script>
<script>
let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 47.603832, lng: -122.330062 },
    zoom: 6,
    mapId: 'acasquetenotes'
  });
  
  {% for city in site.data.cities %}
    new google.maps.marker.AdvancedMarkerElement({
    position: { lat: {{city.lat}}, lng: {{city.long}} }, map: map, title: "{{city.name}}"
  });
  {% endfor %}

}
</script>

<style>
.custom-marker {
  background-color: #ffcc00;
  padding: 5px 10px;
  border-radius: 4px;
  font-weight: bold;
  color: #333;
}
</style>
