

document.getElementById('resetbutton').addEventListener('click', function() {
  const form = document.getElementById('content1');

  // Collect all input fields
  const inputs = form.querySelectorAll('input[type="text"], input[type="radio"], textarea');
  
  // Collect data from the form fields
  const formData = {};
  inputs.forEach(input => {
      if (input.type === 'radio') {
          if (input.checked) {
              formData[input.name] = input.value;
          }
      } else {
          formData[input.name] = input.value;
      }
  });

  // Reset the form fields to their default values
  form.reset();
  alert('Form has been reset!');

  // You can use formData for any further processing if needed
  console.log(formData);
});


document.getElementById('queueStatment').addEventListener('click', function() {
  const form = document.getElementById('content1');
  const url = this.getAttribute('data-url-queue-statement');
  
  // Collect all input fields
  const inputs = form.querySelectorAll('input[type="text"], input[type="radio"], textarea');
  
  // Check if any input fields are empty
  for (const input of inputs) {
      if (input.type === 'radio') {
          // Check if at least one radio button is selected
          const radioGroup = form.querySelectorAll(`input[name="${input.name}"]`);
          const isChecked = Array.from(radioGroup).some(radio => radio.checked);
          if (!isChecked) {
              alert('All fields must be filled out, including selecting a radio button.');
              return; // Break the process if any field is empty
          }
      } else if (!input.value.trim()) {
          alert('All fields must be filled out.');
          return; // Break the process if any field is empty
      }
  }

  // Collect data from the form fields
  const formData = {};
  inputs.forEach(input => {
      if (input.type === 'radio') {
          if (input.checked) {
              formData[input.name] = input.value;
          }
      } else {
          formData[input.name] = input.value;
      }
  });

  // Send data to the server via AJAX
  fetch(url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': '{{ csrf_token }}', // Add your CSRF token here
      },
      body: JSON.stringify(formData),
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          // Reset the form
          form.reset();

          // Alert the user of a successful queue
          alert('Statement queued successfully. Please proceed with the next option.');

          // Disable the selected radio button
          inputs.forEach(input => {
              if (input.type === 'radio' && input.value === formData['default-radio']) {
                  input.disabled = true;
              }
          });
      } else {
          alert('An error occurred while queuing the statement. Please try again.');
      }
  })
  .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while queuing the statement. Please try again.');
  });
});


//Drop Docket Functionality
document.getElementById('dropDocketBtn').addEventListener('click', function() {
  const checkSessionUrl = this.getAttribute('data-url-check-session');
  const clearSessionUrl = this.getAttribute('data-url-clear-session');

  // Check if the session is populated
  fetch(checkSessionUrl, {
      method: 'GET',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': '{{ csrf_token }}', // Add your CSRF token here
      },
  })
  .then(response => response.json())
  .then(data => {
      if (data.session_populated) {
          // Session is populated, proceed to clear it
          fetch(clearSessionUrl, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': '{{ csrf_token }}', // Add your CSRF token here
              },
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  // Reset the form and re-enable all radio buttons
                  const form = document.getElementById('content1');
                  form.reset();

                  // Re-enable all radio buttons
                  const radioButtons = form.querySelectorAll('input[type="radio"]');
                  radioButtons.forEach(radio => {
                      radio.disabled = false;
                  });

                  // Alert the user
                  alert('All session items have been cleared.');
              } else {
                  alert('An error occurred while clearing the session. Please try again.');
              }
          })
          .catch(error => {
              console.error('Error:', error);
              alert('An unexpected error occurred while clearing the session. Please try again.');
          });
      } else {
          // Session is already empty
          alert('The session is already empty. Please start a new docket.');
      }
  })
  .catch(error => {
      console.error('Error:', error);
      alert('An unexpected error occurred while checking the session. Please try again.');
  });
});


//Button to preview the PDF
document.getElementById('previewBtn').addEventListener('click', function() {
    const previewUrl = this.getAttribute('data-url-preview-pdf');

    // Fetch session data
    fetch(previewUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}', // Add your CSRF token here
        },
    })
    .then(response => response.json())
    .then(data => {
        // Check if the docket is empty
        if (Object.keys(data).length === 0) {
            alert('Your docket is empty. Please queue some statements first.');
        } else {
            // Format session data as A4 sheet
            const formattedData = formatAsA4Sheet(data);

            // Display formatted data as modal
            displayModal(formattedData);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An unexpected error occurred while previewing the PDF. Please try again.');
    });
});

// Function to format data as A4 sheet
function formatAsA4Sheet(data) {
    // Your formatting logic here
    let formattedData = '<div class="preview-content">';
    for (const key in data) {
        if (data.hasOwnProperty(key)) {
            formattedData += `<div class="section">${key}</div>`;
            formattedData += `<div class="data">${data[key]}</div>`;
        }
    }
    formattedData += '</div>';
    return formattedData;
}

// Function to display data as modal
function displayModal(formattedData) {
    // Create modal element
    const modal = document.createElement('div');
    modal.classList.add('modal');
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close">&times;</span>
            ${formattedData}
        </div>
    `;
    
    // Append modal to body
    document.body.appendChild(modal);

    // Close modal when close button is clicked
    modal.querySelector('.close').addEventListener('click', function() {
        modal.style.display = 'none';
        document.body.removeChild(modal);
    });

    // Close modal when any part of the screen except the modal panel is clicked
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
            document.body.removeChild(modal);
        }
    });

    // Display modal
    modal.style.display = 'block';
}

















    //Notification dropdown menu
    document.addEventListener('DOMContentLoaded', (event) => {
    const dropdownButtons = [
      {
        button: document.getElementById('dropdownNotificationNameButton'),
        dropdown: document.getElementById('dropdownNotification')
      },
      {
        button: document.getElementById('dropdownNotificationNameButton'),
        dropdown: document.getElementById('dropdownNotification')
      }
    ];

    dropdownButtons.forEach(({ button, dropdown }) => {
      button.addEventListener('click', (event) => {
        dropdown.classList.toggle('hidden');
        event.stopPropagation();
      });
    });

    document.addEventListener('click', (event) => {
      dropdownButtons.forEach(({ dropdown }) => {
        if (!dropdown.classList.contains('hidden')) {
          dropdown.classList.add('hidden');
        }
      });
    });

    dropdownButtons.forEach(({ dropdown }) => {
      dropdown.addEventListener('click', (event) => {
        event.stopPropagation();
      });
    });
  });


// Acocunt dropdown menu
document.addEventListener('DOMContentLoaded', (event) => {
    const button = document.getElementById('dropdownOfficerNameButton');
    const dropdown = document.getElementById('dropdownOfficerName');

    button.addEventListener('click', (event) => {
      dropdown.classList.toggle('hidden');
      event.stopPropagation();
    });

    document.addEventListener('click', (event) => {
      if (!dropdown.classList.contains('hidden')) {
        dropdown.classList.add('hidden');
      }
    });

    dropdown.addEventListener('click', (event) => {
      event.stopPropagation();
    });
  });


    // Get the button and dropdown menu
    const button = document.getElementById('dropdownRadioButton');
    const dropdownMenu = document.getElementById('dropdownDefaultRadio');

    // Toggle dropdown menu visibility
    button.addEventListener('click', () => {
        dropdownMenu.classList.toggle('hidden');
    });

    // Close dropdown menu when clicked outside
    document.addEventListener('click', (event) => {
        const target = event.target;
        if (!button.contains(target) && !dropdownMenu.contains(target)) {
            dropdownMenu.classList.add('hidden');
        }
    });

    // Hide dropdown menu when an item is selected
    const radioInputs = dropdownMenu.querySelectorAll('input[type="radio"]');
    radioInputs.forEach(input => {
        input.addEventListener('change', () => {
            dropdownMenu.classList.add('hidden');
        });
    });



//////////////////////////




  // Get the container element
  const clickedItem = document.getElementById('clicked_item');

    // Get all nav bar elements
    const navBars = document.querySelectorAll('li');

// Add click event listener to each nav bar
navBars.forEach(navBar => {
    navBar.addEventListener('click', () => {
        // Get the text content of the clicked nav bar
        const navBarName = navBar.textContent.trim();

        // Update the content of the clicked_item container
        clickedItem.querySelector('strong').textContent = navBarName;
    });
});



 function showContent(contentId) {
      // Hide all content boxes
      var contentBoxes = document.getElementsByClassName("content-box");
      for (var i = 0; i < contentBoxes.length; i++) {
          contentBoxes[i].classList.add("hidden");
      }

      // Show the selected content box
      document.getElementById(contentId).classList.remove("hidden");
  }

  // Show the default content when the page loads
  showContent('home');






document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('dropdownNotificationButton');
    const dropdown = document.getElementById('dropdownNotification');})

// Dropdown menu for user avatar
document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('dropdownAvatarNameButton');
    const dropdown = document.getElementById('dropdownAvatarName');

    // Toggle dropdown menu visibility
    button.addEventListener('click', function () {
      dropdown.classList.toggle('hidden');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function (event) {
      if (!button.contains(event.target) && !dropdown.contains(event.target)) {
        dropdown.classList.add('hidden');
      }
    });
  });


  document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('dropdownNotificationButton');
    const dropdown = document.getElementById('dropdownNotification');

    // Toggle dropdown menu visibility
    button.addEventListener('click', function () {
      const buttonRect = button.getBoundingClientRect();
      dropdown.style.top = `${buttonRect.bottom}px`;
      dropdown.style.left = `${buttonRect.left}px`;
      dropdown.classList.toggle('hidden');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function (event) {
      if (!button.contains(event.target) && !dropdown.contains(event.target)) {
        dropdown.classList.add('hidden');
      }
    });
  });

            // Get all the tabs
const tabs = document.querySelectorAll('.border-b-2');

// Add event listener to each tab
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove 'active' class from all tabs
        tabs.forEach(t => t.classList.remove('active'));

        // Add 'active' class to the clicked tab
        tab.classList.add('active');
    });
});