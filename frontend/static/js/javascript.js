document.addEventListener("DOMContentLoaded", function(){
    // Get the modal
var modal = document.getElementById("purchaseModal");

var totalMoneyElement = document.getElementById("totalMoney");
var totalMoney = parseInt(totalMoneyElement.textContent);

// NOTE: also have to change to prevent duplicate purchases
var images = document.querySelectorAll(".carousel-img");
images.forEach(function(img){
    img.onclick = function(){
        var priceElement = img.parentElement.querySelector(".price-value");
        var price = parseInt(priceElement.textContent);
        var itemId = img.getAttribute("data-item-id")
    
        modal.style.display = "block";
        var modalText = document.getElementById("modalText")
        // NOTE change name of currency once determined
        modalText.innerHTML = `Confirm Purchase of item for ${price} Rockbux?`

        //check if you're not a brokie b4 purchase
        var confirmButton =document.getElementById("confirmButton");
        confirmButton.onclick = function() {
            if (totalMoney >= price) {
                //send POST request to /shop/unlock route
                fetch('/shop/unlock', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ item_id: itemId })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        totalMoney = data.new_balance;
                        totalMoneyElement.textContent = totalMoney;
                        modalText.innerHTML = "Purchase confirmed!";

                        // Reload the page after 1 second to reflect changes
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

            // Modal auto closes 2 seconds after confirmation or failed purchase
            setTimeout(function (){
                modal.style.display = "none";
            }, 2000);



            } else {
                modalText.innerHTML = "You can't afford this!"
            }     
        }; 
    };  
});


//cancel button
cancelButton.onclick = function () {
    modal.style.display = "none";
};



window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
};
})

