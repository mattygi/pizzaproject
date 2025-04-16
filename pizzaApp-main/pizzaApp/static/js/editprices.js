document.querySelector('.small-btn.login-btn').addEventListener('click', (event) => {
  event.preventDefault(); // Prevent default form submission
  
  // Gather all input values
  const formInputs = document.querySelectorAll('#price-form input[type="number"]');
  const priceData = {};
  
  formInputs.forEach(input => {
      priceData[input.name] = parseFloat(input.value) || 0; // Default to 0 if input is empty
  });

  // Send data to the backend
  fetch('/update_prices', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(priceData)
  })
  .then(response => {
      if (response.ok) {
          alert('Prices updated successfully!');
      } else {
          response.json().then(data => alert('Error: ' + data.error));
      }
  })
  .catch(error => {
      alert('Error: ' + error.message);
  });
});
