let onNextImageSuccess = function (response) {
      if (!response) {
        alert('All images checked.');
        return;
      }

      image_filepath = response[0];
      zoom = response[1];
      num_images_labeled = response[2];
      updateZoom();
    },

    onUpdateZoomSuccess = function (response) {
      image_filepath = response;
      
      $('#zoom-level').html(zoom);
      $('#num-images-labeled').html(num_images_labeled);
      $image.css('opacity', '0');
      $image.attr('src', image_filepath);
      $image.on('load', null);
      $image.on('load', function () {
        $image.css('opacity', '1');
      });

    },
    
    callImagesAPI = function (url, data, successCallback) {
      $.ajax({
        url: url,
        data: JSON.stringify(data),
        type: 'POST',
        contentType: 'application/json',
        success: successCallback,
        error: function(error) {
          console.log(error);
        }
      });
    };

let $image = $('.right-panel img'),

    updateZoom = function () {
      callImagesAPI('/update_zoom', zoom, onUpdateZoomSuccess);
    },

    loadNextImage = function (label) {
      callImagesAPI('/load_next_image', [label, zoom], onNextImageSuccess);
    };

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
  loadNextImage(false);
});

$('#yes-button').click( function (e) {
  loadNextImage(true);
});