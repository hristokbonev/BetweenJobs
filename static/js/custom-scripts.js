$(document).ready(function () {
    $('.selectpicker').selectpicker();

    // Force dropdown to respect page boundaries
    $('.selectpicker').on('shown.bs.select', function () {
      $('.dropdown-menu').css({
        position: 'absolute', /* Ensure it is positioned independently */
        top: 'auto', /* Adjust positioning if needed */
        left: 'auto', /* Adjust positioning if needed */
      });
    });
  });