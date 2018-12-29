let updateZoom = function (newZoom) {
      callImagesAPI('/update_zoom', newZoom, onUpdateZoomSuccess);
    },

    loadNextImage = function (label) {
      callImagesAPI('/load_next_image', label, onNextImageSuccess);
    },

    onNextImageSuccess = function (response) {
      if (!response) {
        alert('All images checked.');
        return;
      }

      image_filepath = response[0];
      zoom = response[1];
      num_images_labeled = response[2];
      
      updateUI();
    },

    onUpdateZoomSuccess = function (response) {
      image_filepath = response[0];
      zoom = response[1]

      updateUI();
    },

    updateUI = function () {
      $('#zoom-level').html(zoom);
      $('#num-images-labeled').html(num_images_labeled);

      let $image = $('.right-panel img');
      $image.css('opacity', '0');
      $image.attr('src', image_filepath);
      $image.on('load', null);
      $image.on('load', function () {
        $image.css('opacity', '1');
      });
    }
    
    callImagesAPI = function (url, data, successCallback) {
      $.ajax({
        url: url,
        data: JSON.stringify(data),
        type: 'POST',
        contentType: 'application/json',
        success: successCallback,
        error: function(xhr, status, error) {
          let responseObj = JSON.parse(xhr.responseText),
              errorMessage = responseObj.message;

          alert(errorMessage);
        }
      });
    };

$('#zoom-in-button').click( function (e) {
  let newZoom = zoom + 1;
  updateZoom(newZoom);
});

$('#zoom-out-button').click( function (e) {
  if (zoom == 0){
    alert('Zoom cannot be negative.')
    return;
  }

  let newZoom = zoom - 1;
  updateZoom(newZoom);
});

$('#no-button').click( function (e) {
  loadNextImage(false);
});

$('#yes-button').click( function (e) {
  loadNextImage(true);
});