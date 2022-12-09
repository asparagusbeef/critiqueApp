$('.like, .dislike').on('click', function() {
    event.preventDefault();
    $('.active').removeClass('active');
    $(this).addClass('active');
});


function onsubmit() {
  var x = document.getElementById("rating");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}