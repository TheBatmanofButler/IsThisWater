mapboxgl.accessToken = 'pk.eyJ1IjoiZ2FuZXNocmF2aWNoYW5kcmFuIiwiYSI6ImNpb3N4anN1cjAwOWl0b201aGp3c2dmN2wifQ.QTc833UD8EWvW0sinlQarg';

let mapboxMap = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/satellite-v9'
    }),

    updateCoords = function (coords) {
      lat = parseFloat(coords['lat']).toFixed(4);
      lng = parseFloat(coords['lng']).toFixed(4);
      
      $('#lat').html(lat);
      $('#lng').html(lng);
    },

    getMapboxURL = function (lng, lat, zoom) {
      return 'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/' + 
             lng + ',' + lat + ',' + zoom + '/400x400?access_token=' +
             mapboxgl.accessToken
    }

mapboxMap.on('mousemove', function (e) {
  let coords = e.lngLat;
  updateCoords(coords);
});

mapboxMap.on('mouseout', function (e) {
  let coords = mapboxMap.getCenter();
  updateCoords(coords);
});

$('#predict-button').click( function (e) {
  let isWater = Math.random() >= 0.5,
      result = isWater ? 'Water detected' : 'No water detected',
      coords = mapboxMap.getCenter(),
      lat = coords['lat'],
      lng = coords['lng'],
      zoom = mapboxMap.getZoom();

  $('#result').html(result);
  $('.static-map').attr('src', getMapboxURL(lng, lat, zoom))
});