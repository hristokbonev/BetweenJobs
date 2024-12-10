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

// >>> Listener function to update selected category in Home page and pass it as form action <<<
function updateSearchFormAction() {
  // Get the selected radio button
  const selectedRadio = document.querySelector('form[name="toggleCategory"] input[name="nav"]:checked');
  
  if (selectedRadio) {
    // Update the search form's action attribute
    const searchForm = document.getElementById('searchForm');
    searchForm.action = selectedRadio.value;

    console.log(`Form action updated to: ${searchForm.action}`);
  }
}

// Attach the 'change' event listener to all radio buttons in the toggleCategory form
document.querySelectorAll('form[name="toggleCategory"] input[name="nav"]').forEach((radio) => {
  radio.addEventListener('change', updateSearchFormAction);
});
