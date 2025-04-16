document.addEventListener("DOMContentLoaded", function () {
    const cartForm = document.getElementById("cart-form");

    if (cartForm) {
        cartForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const method = document.querySelector('input[name="method"]:checked');
            if (!method) {
                alert("Please choose a delivery method.");
                return;
            }

            const selectedMethod = method.value;

            fetch("/proceed", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams({ method: selectedMethod })
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    return response.text();
                }
            })
            .then(data => {
                if (data) {
                    alert(data);
                }
            })
            .catch(error => {
                console.error("Error processing order:", error);
                alert("Something went wrong. Please try again.");
            });
        });
    }
});
