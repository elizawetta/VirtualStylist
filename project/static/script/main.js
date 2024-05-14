function openModal(imagePath) {
    var modal = document.getElementById("myModal");
    var modalImg = document.getElementById("modalImg");
    modal.style.display = "block";
    modalImg.src = imagePath;
    modal.onclick = function(event) {
        if (event.target === modal) {
          closeModal(); 
        }
      };
}
  
function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}
  