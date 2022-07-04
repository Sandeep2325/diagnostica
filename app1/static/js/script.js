$(document).ready(function () {
  const navToggle = document.querySelector(".navbar_toggle");
  const links = document.querySelector(".main_nav");

  navToggle.addEventListener("click", function () {
    links.classList.toggle("show_nav");
  });

  $("#health-care-slider").owlCarousel({
    loop: true,
    margin: 30,
    items: 2,
    responsiveClass: true,
    autoHeight: false,
    autoplayTimeout: 7000,
    smartSpeed: 800,
    dots: false,
    nav: false,
    autoplay: true,
  });
  $("#testimonial_slider").owlCarousel({
    loop: true,
    margin: 30,
    items: 2.7,
    responsiveClass: true,
    autoHeight: false,
    autoplayTimeout: 7000,
    smartSpeed: 800,
    dots: false,
    nav: false,
    autoplay: true,
  });
  
  function codeverify() {
    var digit1 = document.getElementById('verificationCodeDigit1').value;
       if (digit1 == "") {
           alert("OTP is too short");
           return;
       }
       var digit2 = document.getElementById('verificationCodeDigit2').value;
       if (digit2 == "") {
           alert("OTP is too short");
           return;
       }
       var digit3 = document.getElementById('verificationCodeDigit3').value;
       if (digit3 == "") {
           alert("OTP is too short");
           return;
       }
       var digit4 = document.getElementById('verificationCodeDigit4').value;
       if (digit4 == "") {
           alert("OTP is too short");
           return;
       }
       var digit5 = document.getElementById('verificationCodeDigit5').value;
       if (digit5 == "") {
           alert("OTP is too short");
           return;
       }
       var digit6 = document.getElementById('verificationCodeDigit6').value;
       if (digit5 == "") {
           alert("OTP is too short");
           return;
       }
      }
      $(".digit").keyup(function () {
       $(this).next('input').focus();
   });
   
  
   
});
