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
let selectedResumeId = null;

/**
 * Handles resume selection.
 * @param {string} resumeId - The ID of the selected resume.
 * @param {HTMLElement} element - The clicked list item element.
 */
function selectResume(resumeId, element) {
  selectedResumeId = resumeId;

  // Update the "Send Match" button link
  const sendMatchButton = document.getElementById('sendMatchButton');
  sendMatchButton.href = `{{ jobad.id }}/match/${selectedResumeId}`;

  // Remove highlighting from previously selected resume
  document.querySelectorAll('.job-listing').forEach(item => {
    item.classList.remove('selected-resume');
  });

  // Add highlighting to the currently selected resume
  element.classList.add('selected-resume');
};