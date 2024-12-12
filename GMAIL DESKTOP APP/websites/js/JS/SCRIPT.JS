// Smooth scrolling is already handled by CSS's scroll-behavior.
// However, to support older browsers and provide more control, you can use the following JavaScript:

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            window.scrollTo({
                top: target.offsetTop - 70, // Adjust for fixed header height
                behavior: 'smooth'
            });
        }
    });
});

// Optional: Fade-in elements on scroll for enhanced animations
window.addEventListener('scroll', () => {
    const elements = document.querySelectorAll('.animate__animated');
    const windowHeight = window.innerHeight;

    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;

        if (elementTop < windowHeight - 100) { // Trigger 100px before element is in view
            element.classList.add('animate__fadeIn');
        }
    });
});