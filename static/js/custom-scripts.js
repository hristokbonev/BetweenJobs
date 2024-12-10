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


// >>> Resume selector function to hilight resume and store id <<<
// Variable to store the currently selected list item
let activeItem = null;
      
/**
 * Function to handle the addition of the "active" class to a clicked <li>,
 * and update the color of the <a> tag inside it.
 * @param {HTMLElement} element - The clicked list item element.
 */
function setActive(element) {
  // Remove "active" class and reset <a> color for the previously selected item, if any
  if (activeItem) {
    activeItem.classList.remove("active");
    const previousLink = activeItem.querySelector("a");
    if (previousLink) {
      previousLink.style.color = ""; // Reset to default color
    }
  }

  // Add "active" class to the newly clicked item
  element.classList.add("active");

  // Change the color of the <a> tag inside the clicked item to white
  const activeLink = element.querySelector("a");
  if (activeLink) {
    activeLink.style.color = "white";
  }

  // Update the reference to the currently active item
  activeItem = element;
}