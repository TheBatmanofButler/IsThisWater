let $image = $('.right-panel img'),

    getImageSrc = function () {
      return 'https://api.mapbox.com/v4/mapbox.satellite/' + 
            lon + ',' + lat + ',' + zoom + '/1000x1000.png32?access_token='
            + MAPBOX_ACCESS_TOKEN
    },

    updateZoom = function () {
      $('#zoom-level').html(zoom);
      $('#num-images-labeled').html(num_images_labeled);
      $image.css('opacity', '0');
      $image.attr('src', getImageSrc());
      $image.on('load', null);
      $image.on('load', function () {
        $image.css('opacity', '1');
      });
    },

    submitLabel = function (label) {
      $.ajax({
        url: '/load_next_image',
        data: JSON.stringify([label, zoom]),
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
          if (!response) {
            alert('All images checked.');
            return;
          }
    
          lat = response[0];
          lon = response[1];
          zoom = response[2];
          num_images_labeled = response[3];
          updateZoom();
        },
        error: function(error) {
          console.log(error);
        }
      });
    }

$('#zoom-in-button').click( function (e) {
  zoom++;
  updateZoom();
});

$('#zoom-out-button').click( function (e) {
  if (zoom == 0) return;

  zoom--;
  updateZoom();
});

$('#no-button').click( function (e) {
  submitLabel(false);
});

$('#yes-button').click( function (e) {
  submitLabel(true);
});