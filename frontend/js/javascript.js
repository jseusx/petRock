document.addEventListener("DOMContentLoaded", function(){
    // Get the modal
var modal = document.getElementById("purchaseModal");

// Get content of modal
var img = document.getElementById("modalText");
var confirmButton = document.getElementById("confirmButton");
var cancelButton = document.getElementById("cancelButton");

var images = document.querySelectorAll(".carousel-img");
images.forEach(function(img){
    img.onclick = function(){
    modal.style.display = "block";
    modalText.innerHTML = "Confirm Purchase of item?"
    };  
});


//cancel button
cancelButton.onclick = function () {
    modal.style.display = "none";
};

//confirm button
confirmButton.onclick = function() {
    alert("Purchase confirmed!");
    modal.style.display = "none";
}; 

//found this cool thing randomly it closes the model if you click outside of it
window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
};
})

