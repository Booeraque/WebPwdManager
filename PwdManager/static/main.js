// Get all buttons
const buttons = document.querySelectorAll('.dashboard__button');

// Add click event listener to each button
buttons.forEach(button => {
    button.addEventListener('click', function() {
        // Remove selected class from all buttons
        buttons.forEach(btn => btn.classList.remove('selected'));

        // Add selected class to clicked button
        this.classList.add('selected');
    });
});