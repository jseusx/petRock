document.addEventListener("DOMContentLoaded", function(){
    // Get the modal
var modal = document.getElementById("purchaseModal");

// Get content of modal
// var confirmButton = document.getElementById("confirmButton");
// var cancelButton = document.getElementById("cancelButton");

//NOTE: for demo purposes, this value really should be read from the database so its user specific
var totalMoneyElement = document.getElementById("totalMoney");
var totalMoney = parseInt(totalMoneyElement.textContent);

// NOTE: also have to change to prevent duplicate purchases
var images = document.querySelectorAll(".carousel-img");
images.forEach(function(img){
    img.onclick = function(){
        var priceElement = img.parentElement.querySelector(".price-value");
        var price = parseInt(priceElement.textContent);
    
        modal.style.display = "block";
        // NOTE change name of currency once determined
        modalText.innerHTML = `Confirm Purchase of item for ${price} dabloons?`

        //check if you're not a brokie b4 purchase
        confirmButton.onclick = function() {
            if (totalMoney >= price) {
                totalMoney -= price;
                totalMoneyElement.textContent = totalMoney;
                modalText.innerHTML = "Purchase confirmed!"
            }
            else {
                modalText.innerHTML = "You can't afford this!"
            }

            // Modal auto closes 2 seconds after confirmation or failed purchase
            setTimeout(function (){
                modal.style.display = "none";
            }, 2000)
        }; 
    };  
});


//cancel button
cancelButton.onclick = function () {
    modal.style.display = "none";
};



//found this cool thing randomly it closes the model if you click outside of it
window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
};
})

