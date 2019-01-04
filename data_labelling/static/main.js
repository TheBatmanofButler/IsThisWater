let updateZoom = function (newZoom) {
      callImagesAPI('/update_zoom', newZoom, false);
    },

    loadNextImage = function (label) {
      callImagesAPI('/load_next_image', label, true);
    },

    serverCallback = function (response, prepForNextImage) {
      if (prepForNextImage) {
        num_images_left = response['num_images_left'];
        next_image_is_ready = response['next_image_is_ready'];
  
        if (next_image_is_ready === false) {
          $('.button')
            .off('click')
            .on('click', function () {
              alert('All sites have been labeled.');
            });
        }
      }

      image_filepath = response['image_filepath'];
      zoom = response['zoom'];

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
    }
    
    callImagesAPI = function (url, data, prepForNextImage) {
      $.ajax({
        url: url,
        data: JSON.stringify(data),
        type: 'POST',
        contentType: 'application/json',
        success: function (response) {
          serverCallback(response, prepForNextImage);
        },
        error: function(xhr, status, error) {
          let responseObj = JSON.parse(xhr.responseText),
              errorMessage = responseObj.message;

          alert(errorMessage);
        },
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