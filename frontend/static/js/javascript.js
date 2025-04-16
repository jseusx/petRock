document.addEventListener("DOMContentLoaded", function () {
    // Get the modal
    var modal = document.getElementById("purchaseModal");
    var modalText = document.getElementById("modalText");
    var cancelButton = document.getElementById("cancelButton");
    var confirmButton = document.getElementById("confirmButton");
    var totalMoneyElement = document.getElementById("totalMoney");
    var totalMoney = parseInt(totalMoneyElement.textContent);
    var currentItem = null;

    // Handle Buy button clicks
    var buyButtons = document.querySelectorAll(".buy-button");
    buyButtons.forEach(function (button) {
        button.onclick = function () {
            var itemName = button.getAttribute("data-item-name");
            var itemPrice = parseInt(button.getAttribute("data-item-price"));
            var itemId = button.getAttribute("data-item-id");

            currentItem = { id: itemId, name: itemName, price: itemPrice };

            modalText.innerHTML = `Confirm Purchase of ${itemName} for ${itemPrice} Rockbux?`;
            modal.style.display = "block";
        };
    });

    // Confirm button functionality
    confirmButton.onclick = function () {
        if (currentItem && totalMoney >= currentItem.price) {
            // Send POST request to /shop/unlock route
            fetch('/shop/unlock', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ item_id: currentItem.id })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        totalMoney = data.new_balance;
                        totalMoneyElement.textContent = totalMoney;
                        modalText.innerHTML = "Purchase confirmed!";
                        setTimeout(function () {
                            location.reload();
                        }, 1000);
                    } else {
                        modalText.innerHTML = data.error || "An error occurred.";
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    modalText.innerHTML = "An error occurred.";
                });

            setTimeout(function () {
                modal.style.display = "none";
            }, 2000);
        } else {
            modalText.innerHTML = "You can't afford this!";
        }
    };

    // Cancel button functionality
    cancelButton.onclick = function () {
        modal.style.display = "none";
    };

    // Close modal when clicking outside
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
});