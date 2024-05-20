document.addEventListener('DOMContentLoaded', function() {
    const resetButton = document.getElementById('resetbutton');
    const dropDocketButton = document.getElementById('dropDocketBtn');
    const previewButton = document.getElementById('previewBtn');
    const queueButton = document.getElementById('queueStatment');
    const generatePDFButton = document.getElementById('docketpdf');

    resetButton.addEventListener('click', function() {
        document.getElementById('content1').reset();
    });

    dropDocketButton.addEventListener('click', function() {
        fetch('{% url "drop_docket" %}', {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => response.json())
        .then(data => {
            alert('Docket dropped successfully');
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while dropping the docket.');
        });
    });

    previewButton.addEventListener('click', function() {
        let formData = new FormData(document.getElementById('content1'));
        fetch('{% url "preview_pdf" %}', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => response.json())
        .then(data => {
            const modal = document.createElement('div');
            modal.id = 'previewModal';
            modal.innerHTML = `
                <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center;">
                    <div style="background: white; padding: 20px; position: relative;">
                        <button id="closeModal" style="position: absolute; top: 10px; right: 10px;">&times;</button>
                        <embed src="data:application/pdf;base64,${data.pdf_content}" width="600" height="500" type="application/pdf">
                    </div>
                </div>
            `;
            document.body.appendChild(modal);

            document.getElementById('closeModal').addEventListener('click', function() {
                document.body.removeChild(modal);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while generating the preview.');
        });
    });

    queueButton.addEventListener('click', function(event) {
        event.preventDefault();
        let formData = new FormData(document.getElementById('content1'));
        fetch('{% url "queue_statement" %}', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'error') {
                alert(data.message);
                resetButton.click();
            } else {
                alert('Statement queued successfully');
                document.getElementById('content1').reset();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Empty: Cannot Que Empty Session');
        });
    });

    generatePDFButton.addEventListener('click', function(event) {
        event.preventDefault();
        let formData = new FormData(document.getElementById('content1'));
        fetch('{% url "generate_pdf" %}', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => response.blob())
        .then(blob => {
            // Convert blob to URL
            const url = window.URL.createObjectURL(blob);
            
            // Save PDF to database (if needed) and download it
                    fetch('{% url "save_pdf" %}', {
                method: 'POST',
                body: blob,
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/pdf'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error('There was a problem with your fetch operation:', error);
            });

            // Download PDF
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'docket.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.getElementById('content1').reset();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while generating the PDF.');
        });
    });
});



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