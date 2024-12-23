document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const signInLink = document.getElementById('signInLink');
    const signInModal = new bootstrap.Modal(document.getElementById('signInModal'));
    const signInForm = document.getElementById('signInForm');
    const errorMessage = document.getElementById('error-message');

    // Show the modal when Sign In is clicked
    signInLink.addEventListener('click', function(event) {
        event.preventDefault();
        signInModal.show();
    });

    // Handle form submission
    signInForm.addEventListener('submit', function(event) {
        event.preventDefault();

        // Get the email and password values
        const email = document.getElementById('emailInput').value;
        const password = document.getElementById('passwordInput').value;

        // Fetch login data from API using GET request
        fetch('http://13.201.126.238:8055/items/log_in', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            return response.json(); // Parse the response as JSON
        })
        .then(data => {
            console.log('Fetched data:', data);

            // Assuming the API returns an array of login records in data.data
            const loginRecords = data.data;

            // Check if the email and password match any record
            const user = loginRecords.find(record => record.email_id === email && record.password === password);

            if (user) {
                // Login successful, redirect to home.html
                window.location.href = 'start';
            } else {
                // Login failed, show error message
                errorMessage.textContent = 'Incorrect email or password. Please try again.';
                errorMessage.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessage.textContent = 'An error occurred. Please try again later.';
            errorMessage.style.display = 'block';
        });
    });
});
