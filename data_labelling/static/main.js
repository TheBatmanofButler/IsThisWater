let updateZoom = function (newZoom) {
      callImagesAPI('/update_zoom', newZoom, onUpdateZoomSuccess);
    },

    loadNextImage = function (label) {
      callImagesAPI('/load_next_image', label, onNextImageSuccess);
    },

    onNextImageSuccess = function (response) {
      image_filepath = response['image_filepath'];
      zoom = response['zoom'];
      num_images_left = response['num_images_left'];
      next_image_is_ready = response['next_image_is_ready']

      if (!next_image_is_ready)
        $('.button').off();
      
      updateUI();
    },

    onUpdateZoomSuccess = function (response) {
      image_filepath = response[0];
      zoom = response[1]

      updateUI();
    },

    updateUI = function () {
      $('#zoom-level').html(zoom);
      $('#num-images-left').html(num_images_left);

      let $image = $('.right-panel img');
      $image.css('opacity', '0');
      $image.attr('src', image_filepath);
      $image.on('load', null);
      $image.on('load', function () {
        $image.css('opacity', '1');
      });
      console.log(222);
    }
    
    callImagesAPI = function (url, data, successCallback) {
      $.ajax({
        url: url,
        data: JSON.stringify(data),
        type: 'POST',
        contentType: 'application/json',
        success: successCallback
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
  loadNextImage(0);
});

$('#yes-button').click( function (e) {
  loadNextImage(1);
});

$('#ignore-button').click( function (e) {
  loadNextImage(2);
});