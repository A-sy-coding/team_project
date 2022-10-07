var slideWrapper = document.querySelector('.s-box');
var slides = document.querySelectorAll('.item-s');
var totalSlides = slides.length; // item의 갯수


var sliderWidth = slideWrapper.clientWidth; // container의 width
var slideIndex = 0;
var slider = document.querySelector('.slide-s');

slider.style.width = sliderWidth * totalSlides + 'px';

showSlides()

function showSlides() {
    for(var i=0;i<slides.length;i++){
        slider.style.left = -(sliderWidth * slideIndex) + 'px';    
    }
    slideIndex++;
    if (slideIndex === totalSlides) {
        slideIndex = 0;
    }
    setTimeout(showSlides, 2500); 
}