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
  
function selectAll() {
  
  var checkboxes = document.querySelectorAll('.btn-check');
  var allChecked = true;

  checkboxes.forEach(function(checkbox) {
    if (!checkbox.checked) {
      allChecked = false;
    }
  });

  checkboxes.forEach(function(checkbox) {
    checkbox.checked = !allChecked;
  });
  event.preventDefault();
}