// Get all buttons
const buttons = document.querySelectorAll('.dashboard__button');

// Add click event listener to each button
buttons.forEach(button => {
    button.addEventListener('click', function() {
        // Remove selected class from all buttons
        buttons.forEach(btn => btn.classList.remove('selected'));

        // Add selected class to clicked button
        this.classList.add('selected');
    });
});

// Get the form
const form = document.querySelector('.save__pass');

// Get the Generate button
const generateButton = document.querySelector('#generate');

// Add click event listener to the Generate button
generateButton.addEventListener('click', function() {
    // Get password options
    const length = document.querySelector('.password-length').value;
    const useUppercase = document.querySelector('.password-uppercase').checked;
    const useNumbers = document.querySelector('.password-numbers').checked;
    const useSymbols = document.querySelector('.password-symbols').checked;

    // Make the fetch request
    fetch('/generate_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            length: length,
            useUppercase: useUppercase,
            useNumbers: useNumbers,
            useSymbols: useSymbols
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Fill in the password field with the generated password
        document.querySelector('.gen--pass').value = data.password;
    })
    .catch((error) => {
      console.error('Error:', error);
    });
});

// Add submit event listener to the form
form.addEventListener('submit', function(event) {
    // Prevent the form from submitting normally
    event.preventDefault();

    // Get input fields
    const websiteField = document.querySelector('.gen--website');
    const usernameField = document.querySelector('.gen--username');
    const passwordField = document.querySelector('.gen--pass');

    // Make the fetch request
    fetch('/save_pass', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            website: websiteField.value,
            username: usernameField.value,
            password: passwordField.value
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Clear the input fields
        websiteField.value = '';
        usernameField.value = '';
        passwordField.value = '';

        // Display a success message
        const message = document.querySelector('.success__message');
        message.textContent = 'Password saved successfully!';
    })
    .catch((error) => {
      console.error('Error:', error);
    });
});

// Get the "View All Passwords" button
const viewAllPasswordsButton = document.querySelector('.btn--two');

// Add click event listener to the button
viewAllPasswordsButton.addEventListener('click', function() {
    // Fetch the passwords from the server
    fetch('/get_pass')
        .then(response => response.json())
        .then(data => {
            // Get the password list div
            const passwordListDiv = document.getElementById('password-list');

            // Clear the div
            passwordListDiv.innerHTML = '';

            // Insert the passwords into the div
            data.passwords.forEach(password => {
                passwordListDiv.innerHTML += `
                    <p>
                        Website: ${password.website}<br>
                        Username: ${password.username}<br>
                        Password: ${password.password}<br>
                    </p>
                `;
            });

            // Hide the dashboard__main--right div
            document.querySelector('.dashboard__main--right').style.display = 'none';

            // Display the password list div
            passwordListDiv.style.display = 'block';
        });
});

// Get the "Dashboard" button
const dashboardButton = document.querySelector('#dashboard-button');

// Add click event listener to the button
dashboardButton.addEventListener('click', function() {
    // Navigate to the dashboard
    window.location.href = '/dashboard';
});