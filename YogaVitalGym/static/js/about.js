
$(document).ready(function(){
  var currentIndex = 0;
  var slides = $('.slide');
  var slideCount = slides.length;

  function showSlide(index) {
    slides.removeClass('active');
    slides.eq(index).addClass('active');
  }

  function nextSlide() {
    currentIndex = (currentIndex + 1) % slideCount;
    showSlide(currentIndex);
  }

  setInterval(nextSlide, 10000); // Change slide every 10 seconds
});



$(document).ready(function(){
  var currentIndex = 0;
  var slides = $('.slide-1');
  var slideCount = slides.length;

  function showSlide(index) {
    slides.removeClass('active');
    slides.eq(index).addClass('active');
  }

  function nextSlide() {
    currentIndex = (currentIndex + 1) % slideCount;
    showSlide(currentIndex);
  }

  setInterval(nextSlide, 10000); // Change slide every 10 seconds
});