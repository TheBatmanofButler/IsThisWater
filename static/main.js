$('.result-row').click(function () {
//  $(this).child('.remove-box'). 
  if ($(this).hasClass('selected')) {
    $(this).removeClass('selected');
    // $(this).css('background', 'red');
  }
  else {
    $(this).addClass('selected');
    // $(this).css('background', '#fff');
  }
});

$("table").stickyTableHeaders();