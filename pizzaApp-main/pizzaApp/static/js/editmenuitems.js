document.addEventListener("DOMContentLoaded", () => {
  const deleteButtons = document.querySelectorAll("button[value='delete']");

  deleteButtons.forEach(button => {
    button.addEventListener("click", event => {
      if (!confirm("Are you sure you want to delete this item?")) {
        event.preventDefault(); // Prevent form submission
      }
    });
  });
});
