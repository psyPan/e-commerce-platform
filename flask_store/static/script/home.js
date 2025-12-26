const track = document.getElementById('sliderTrack');
const dots = document.querySelectorAll('.dot');
let currentSlide = 0;
const totalSlides = 2; // Change this if you add more slides
let slideInterval;
// Function to update the position of the track
function updateSlider() {
    const translateX = -(currentSlide * 100);
    track.style.transform = `translateX(${translateX}%)`;
    // Update dots visual
    dots.forEach((dot, index) => {
        if (index === currentSlide) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    });
}
// Go to next slide (loops back to 0)
function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    updateSlider();
}
// Go to specific slide (when clicking dots)
function goToSlide(index) {
    currentSlide = index;
    updateSlider();
    resetTimer(); // Reset timer so it doesn't jump immediately after you click
}
function resetTimer() {
    clearInterval(slideInterval);
    slideInterval = setInterval(nextSlide, 5000); // 5000ms = 5 seconds
}
// Start the timer on load
resetTimer();