document.addEventListener("DOMContentLoaded", () => {
  const pizzaSelect = document.getElementById("pizza");
  const quantityInput = document.getElementById("quantity");

  // Handle "Select All" and "Clear" functionality for meat and veggie checkboxes
  function updateCheckboxes(groupName, action) {
    const checkboxes = document.querySelectorAll(`input[name='${groupName}']`);
    checkboxes.forEach(cb => cb.checked = action === "select");
  }

  document.querySelector(".select-btn").addEventListener("click", () => updateCheckboxes("meats", "select"));
  document.querySelector(".clear-btn").addEventListener("click", () => updateCheckboxes("meats", "clear"));
  document.querySelector(".select-btn").addEventListener("click", () => updateCheckboxes("veggies", "select"));
  document.querySelector(".clear-btn").addEventListener("click", () => updateCheckboxes("veggies", "clear"));

  // Submit form and send data to backend
  document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const selectedPizza = pizzaSelect.value;
    const size = document.querySelector("input[name='size']:checked")?.value;
    const crust = document.querySelector("input[name='crust']:checked")?.value;
    const meats = Array.from(document.querySelectorAll("input[name='meats']:checked")).map(cb => cb.value);
    const veggies = Array.from(document.querySelectorAll("input[name='veggies']:checked")).map(cb => cb.value);
    const quantity = quantityInput.value;

    const pizzaData = {
      pizzaType: selectedPizza,
      size,
      crust,
      meats,
      veggies,
      quantity
    };

    // Send data to backend
    try {
      const response = await fetch("/customize_pizza", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(pizzaData)
      });
      const result = await response.json();
      alert(`Added to cart: ${result.message}`);
    } catch (error) {
      alert("Failed to add to cart. Try again later.");
    }
  });
});
