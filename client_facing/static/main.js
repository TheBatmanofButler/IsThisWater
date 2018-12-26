mapboxgl.accessToken = 'pk.eyJ1IjoiZ2FuZXNocmF2aWNoYW5kcmFuIiwiYSI6ImNpb3N4anN1cjAwOWl0b201aGp3c2dmN2wifQ.QTc833UD8EWvW0sinlQarg';

let mapboxMap = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v11'
});

mapboxMap.on('mousemove', function (e) {
  let coords = e.lngLat;
  
  lat = coords['lat'];
  lng = coords['lng'];
  
  console.log(coords);
  $('#lat').html(lat);
  $('#lng').html(lng);
});

mapboxMap.on('click', function (e) {
  let isWater = Math.random() >= 0.5,
      result = isWater ? 'Water detected' : 'No water detected';

  $('#result').html(result);
});