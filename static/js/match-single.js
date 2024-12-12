// Variable to store the currently selected list item
let activeItem = null;

function setActive(element) {
    // Remove the "active" class from the previously selected item, if any
    if (activeItem) {
        activeItem.classList.remove("active");
    }

    // Add the "active" class to the clicked item
    element.classList.add("active");

    // Get the resume ID from the clicked item
    const resumeId = element.getAttribute("data-id");

    // Update the form's action attribute dynamically
    const applyForm = document.querySelector("form[action]");

    if (applyForm) {
      const jobId = applyForm.querySelector("button").getAttribute("data-job-id");
      if (jobId){
        // Set the action URL with both jobId and resumeId
        applyForm.setAttribute("action", `/match/${jobId}/match/${resumeId}`);
      }
    }

    // Update the reference to the currently active item
    activeItem = element;
}