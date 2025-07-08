document.addEventListener('DOMContentLoaded', function() {
    // Like button functionality
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('active');
            const icon = this.querySelector('i');
            if (this.classList.contains('active')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
            }
            
            // In a real app, you would send an AJAX request here
            const movieId = this.getAttribute('data-movie-id');
            console.log(`Liked movie ID: ${movieId}`);
        });
    });
    
    // Filter form submission
    const filterForm = document.querySelector('.sidebar form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // In a real app, you would send the filter data to the server
            console.log('Filters applied');
        });
    }
});