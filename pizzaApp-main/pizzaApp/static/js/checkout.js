document.querySelector('form').addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent default form submission

    // Gather form data
    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Send the data to the backend
    fetch('/checkout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        if (response.ok) {
            alert(result.message); // Success message
        } else {
            alert('Error: ' + result.error); // Error message
        }
    })
    .catch(error => {
        alert('Error: ' + error.message); // Handle network errors
    });
});
