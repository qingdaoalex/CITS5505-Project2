mapboxgl.accessToken = 'pk.eyJ1IjoieXVuZmFuZyIsImEiOiJjbHcwcGVyeTcwM21xMmpxc2pnazg1Mm55In0.e5hDDcbk1KiDDIZEGWMECg';
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v11',
  center: [100.9, 34.2],
  zoom: 1,
  projection: 'globe'
});

map.addControl(new mapboxgl.NavigationControl());
map.scrollZoom.disable();